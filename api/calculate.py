from http.server import BaseHTTPRequestHandler
import json, math, datetime, zoneinfo
import swisseph as swe

SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
PLANETS={'Sun':swe.SUN,'Moon':swe.MOON,'Mars':swe.MARS,'Mercury':swe.MERCURY,'Jupiter':swe.JUPITER,'Venus':swe.VENUS,'Saturn':swe.SATURN,'Rahu':swe.MEAN_NODE}
NAKS=['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','Purva Ashadha','Uttara Ashadha','Shravana','Dhanishtha','Shatabhisha','Purva Bhadrapada','Uttara Bhadrapada','Revati']
LORDS=['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']; YEARS={'Ketu':7,'Venus':20,'Sun':6,'Moon':10,'Mars':7,'Rahu':18,'Jupiter':16,'Saturn':19,'Mercury':17}
swe.set_sid_mode(swe.SIDM_LAHIRI)

def calc(payload):
    dt=datetime.date.fromisoformat(payload['date']); tm=datetime.time.fromisoformat(payload['time'])
    tz=zoneinfo.ZoneInfo(payload.get('timezone') or 'Asia/Kolkata')
    local=datetime.datetime.combine(dt,tm).replace(tzinfo=tz); utc=local.astimezone(datetime.timezone.utc)
    jd=swe.julday(utc.year,utc.month,utc.day,utc.hour+utc.minute/60+utc.second/3600)
    flags=swe.FLG_SWIEPH|swe.FLG_SIDEREAL
    cusps,ascmc=swe.houses_ex(jd,float(payload.get('lat',0)),float(payload.get('lon',0)),b'P',swe.FLG_SIDEREAL)
    asc=ascmc[0]%360; asc_sign=int(asc//30)
    ps=[]
    for name,code in PLANETS.items():
        xx,_=swe.calc_ut(jd,code,flags); lon=xx[0]%360
        ps.append({'name':name,'longitude':lon,'sign':int(lon//30),'sign_name':SIGNS[int(lon//30)],'degree':lon%30,'house':((int(lon//30)-asc_sign)%12)+1})
    # Ketu opposite Rahu
    rah=[p for p in ps if p['name']=='Rahu'][0]; klon=(rah['longitude']+180)%360
    ps.append({'name':'Ketu','longitude':klon,'sign':int(klon//30),'sign_name':SIGNS[int(klon//30)],'degree':klon%30,'house':((int(klon//30)-asc_sign)%12)+1})
    moon=next(p for p in ps if p['name']=='Moon'); nak_span=360/27; ni=int(moon['longitude']//nak_span); frac=(moon['longitude']%nak_span)/nak_span
    nak={'name':NAKS[ni],'number':ni+1,'pada':min(4,int(frac*4)+1)}
    # simple D9 mapping
    d9ps=[]
    for p in ps:
        sign=p['sign']; deg=p['degree']; part=int(deg/(30/9)); d9sign=(sign*9+part)%12
        d9ps.append({'name':p['name'],'sign':d9sign,'sign_name':SIGNS[d9sign],'degree':(deg%(30/9))*9})
    # Vimshottari periods from Moon nakshatra
    lord=LORDS[ni]; elapsed=frac*YEARS[lord]; remaining=YEARS[lord]-elapsed
    start=local-datetime.timedelta(days=elapsed*365.2425)
    periods=[]; cur=start
    for i in range(9):
        l=LORDS[(LORDS.index(lord)+i)%9]; dur=remaining if i==0 else YEARS[l]; end=cur+datetime.timedelta(days=dur*365.2425)
        periods.append({'lord':l,'start':cur.date().isoformat(),'end':end.date().isoformat(),'years':dur}); cur=end
    return {'input':payload,'jd_ut':jd,'lagna':{'longitude':asc,'sign':asc_sign,'sign_name':SIGNS[asc_sign]},'planets':ps,'nakshatra':nak,'d9':{'planets':d9ps},'vimshottari':{'mahadasha':periods}}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            n=int(self.headers.get('content-length','0')); payload=json.loads(self.rfile.read(n) or '{}')
            if not payload.get('date') or not payload.get('time'): raise ValueError('date and time are required')
            result=calc(payload); self.send_response(200)
            self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps(result,default=str).encode())
        except Exception as e:
            self.send_response(400); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps({'error':str(e)}).encode())
