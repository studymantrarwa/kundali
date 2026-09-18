from http.server import BaseHTTPRequestHandler
import json, os, urllib.parse, urllib.request

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            n=int(self.headers.get('content-length','0')); data=json.loads(self.rfile.read(n) or '{}')
            key=os.environ.get('GOOGLE_TIMEZONE_SERVER_KEY')
            if not key: raise Exception('GOOGLE_TIMEZONE_SERVER_KEY is not configured')
            lat=float(data['lat']); lng=float(data['lng']); ts=int(data.get('timestamp',0))
            url='https://maps.googleapis.com/maps/api/timezone/json?'+urllib.parse.urlencode({'location':f'{lat},{lng}','timestamp':ts,'key':key})
            with urllib.request.urlopen(url,timeout=10) as r: result=json.loads(r.read())
            self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps({'error':str(e)}).encode())
