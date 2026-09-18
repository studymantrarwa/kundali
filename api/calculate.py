from http.server import BaseHTTPRequestHandler
import json
import datetime
import zoneinfo
import swisseph as swe


# =========================================================
# STUDY MANTRA - KUNDLI CALCULATION ENGINE
# Swiss Ephemeris + Lahiri Ayanamsha
# =========================================================

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
}

NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishtha",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

# =========================================================
# VIMSHOTTARI DASHA ORDER
# =========================================================

DASHA_LORDS = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
]

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

TOTAL_DASHA_YEARS = 120.0

# Average astronomical year
YEAR_DAYS = 365.2425

# Lahiri ayanamsha
swe.set_sid_mode(swe.SIDM_LAHIRI)


# =========================================================
# HELPERS
# =========================================================

def norm360(value):
    return float(value) % 360.0


def sign_index(longitude):
    return int(norm360(longitude) // 30)


def sign_name(longitude):
    return SIGNS[sign_index(longitude)]


def planet_result(jd, planet_id, flags):
    """
    Compatible with different pyswisseph return formats.
    """

    result = swe.calc_ut(
        jd,
        planet_id,
        flags
    )

    if isinstance(result, tuple):
        return result[0]

    return result


def get_ayanamsha(jd):
    """
    Get Lahiri ayanamsha.
    """

    try:
        return float(
            swe.get_ayanamsa_ut(jd)
        )
    except Exception:

        try:
            return float(
                swe.get_ayanamsa(jd)
            )
        except Exception:
            return 0.0


def tropical_to_sidereal(
    longitude,
    ayanamsha
):
    return norm360(
        longitude - ayanamsha
    )


def add_years(
    date_time,
    years
):
    return date_time + datetime.timedelta(
        days=float(years) * YEAR_DAYS
    )


# =========================================================
# HOUSE / ASCENDANT
# =========================================================

def calculate_houses(
    jd,
    latitude,
    longitude
):
    """
    Use swe.houses().

    This keeps compatibility with pyswisseph versions
    where houses_ex() may return different structures.
    """

    result = swe.houses(
        float(jd),
        float(latitude),
        float(longitude),
        b"P"
    )

    if not isinstance(result, tuple):
        raise RuntimeError(
            "Swiss Ephemeris houses() returned an unexpected result."
        )

    if len(result) < 2:
        raise RuntimeError(
            "Swiss Ephemeris houses() returned incomplete house data."
        )

    cusps = result[0]
    ascmc = result[1]

    if len(ascmc) < 1:
        raise RuntimeError(
            "Swiss Ephemeris did not return Ascendant data."
        )

    tropical_asc = norm360(
        float(ascmc[0])
    )

    ayanamsha = get_ayanamsha(
        jd
    )

    sidereal_asc = tropical_to_sidereal(
        tropical_asc,
        ayanamsha
    )

    return {
        "cusps": cusps,
        "ascendant": sidereal_asc,
        "ayanamsha": ayanamsha,
    }


# =========================================================
# NAKSHATRA
# =========================================================

def calculate_nakshatra(
    moon_longitude
):
    nakshatra_span = 360.0 / 27.0

    moon_longitude = norm360(
        moon_longitude
    )

    index = int(
        moon_longitude / nakshatra_span
    )

    if index < 0:
        index = 0

    if index > 26:
        index = 26

    inside = (
        moon_longitude
        - index * nakshatra_span
    )

    fraction = (
        inside / nakshatra_span
    )

    pada = int(
        fraction * 4
    ) + 1

    if pada < 1:
        pada = 1

    if pada > 4:
        pada = 4

    lord = DASHA_LORDS[
        index % 9
    ]

    return {
        "name": NAKSHATRAS[index],
        "number": index + 1,
        "pada": pada,
        "lord": lord,
        "longitude": moon_longitude,
    }


# =========================================================
# NAVAMSA / D9
# =========================================================

def calculate_navamsa(
    planet
):

    longitude = norm360(
        planet["longitude"]
    )

    sign = int(
        longitude // 30
    )

    degree = (
        longitude % 30
    )

    navamsa_part = int(
        degree / (30.0 / 9.0)
    )

    if navamsa_part < 0:
        navamsa_part = 0

    if navamsa_part > 8:
        navamsa_part = 8

    d9_sign = (
        sign * 9
        + navamsa_part
    ) % 12

    d9_degree = (
        degree % (30.0 / 9.0)
    ) * 9.0

    d9_longitude = norm360(
        d9_sign * 30
        + d9_degree
    )

    return {
        "name": planet["name"],
        "longitude": d9_longitude,
        "sign": d9_sign,
        "sign_name": SIGNS[d9_sign],
        "degree": d9_degree,
    }


# =========================================================
# DASHA - PRATYANTARDASHA
# =========================================================

def calculate_pratyantardasha(
    antar_lord,
    antar_start,
    antar_end
):
    """
    9 Pratyantardasha periods inside one Antardasha.

    Sequence starts from the Antardasha lord.
    """

    total_seconds = (
        antar_end - antar_start
    ).total_seconds()

    if total_seconds <= 0:
        return []

    periods = []

    start_index = DASHA_LORDS.index(
        antar_lord
    )

    current = antar_start

    for i in range(9):

        lord = DASHA_LORDS[
            (start_index + i) % 9
        ]

        proportion = (
            DASHA_YEARS[lord]
            / TOTAL_DASHA_YEARS
        )

        duration_seconds = (
            total_seconds
            * proportion
        )

        end = (
            current
            + datetime.timedelta(
                seconds=duration_seconds
            )
        )

        periods.append({
            "lord": lord,
            "start": current.isoformat(),
            "end": end.isoformat(),
            "years": (
                DASHA_YEARS[lord]
                * (
                    (
                        antar_end
                        - antar_start
                    ).total_seconds()
                    / 86400.0
                )
                / YEAR_DAYS
                / TOTAL_DASHA_YEARS
            ),
        })

        current = end

    # Make sure final end is exact
    if periods:
        periods[-1]["end"] = (
            antar_end.isoformat()
        )

    return periods


# =========================================================
# DASHA - ANTARDASHA
# =========================================================

def calculate_antardasha(
    maha_lord,
    maha_start,
    maha_end
):
    """
    9 Antardasha periods inside one Mahadasha.

    Sequence starts from Mahadasha lord.
    """

    total_seconds = (
        maha_end - maha_start
    ).total_seconds()

    if total_seconds <= 0:
        return []

    periods = []

    start_index = DASHA_LORDS.index(
        maha_lord
    )

    current = maha_start

    maha_years = (
        DASHA_YEARS[maha_lord]
    )

    for i in range(9):

        lord = DASHA_LORDS[
            (start_index + i) % 9
        ]

        proportion = (
            DASHA_YEARS[lord]
            / TOTAL_DASHA_YEARS
        )

        duration_seconds = (
            total_seconds
            * proportion
        )

        end = (
            current
            + datetime.timedelta(
                seconds=duration_seconds
            )
        )

        # Antardasha duration in years
        antar_years = (
            maha_years
            * DASHA_YEARS[lord]
            / TOTAL_DASHA_YEARS
        )

        # Pratyantardasha
        pratyantar = (
            calculate_pratyantardasha(
                lord,
                current,
                end
            )
        )

        periods.append({
            "lord": lord,
            "start": current.isoformat(),
            "end": end.isoformat(),
            "years": antar_years,
            "pratyantardasha": pratyantar,
        })

        current = end

    # Exact final boundary
    if periods:
        periods[-1]["end"] = (
            maha_end.isoformat()
        )

        if periods[-1]["pratyantardasha"]:
            periods[-1][
                "pratyantardasha"
            ][-1]["end"] = (
                maha_end.isoformat()
            )

    return periods


# =========================================================
# VIMSHOTTARI MAHADASHA
# =========================================================

def calculate_vimshottari(
    moon_longitude,
    birth_local
):
    """
    Vimshottari Dasha based on sidereal Moon longitude.

    Returns:

        Mahadasha
          └── Antardasha
                └── Pratyantardasha
    """

    moon_longitude = norm360(
        moon_longitude
    )

    nakshatra_span = (
        360.0 / 27.0
    )

    nak_index = int(
        moon_longitude
        / nakshatra_span
    )

    if nak_index < 0:
        nak_index = 0

    if nak_index > 26:
        nak_index = 26

    inside_nakshatra = (
        moon_longitude
        - nak_index * nakshatra_span
    )

    fraction_completed = (
        inside_nakshatra
        / nakshatra_span
    )

    first_lord = DASHA_LORDS[
        nak_index % 9
    ]

    first_total_years = (
        DASHA_YEARS[first_lord]
    )

    elapsed_years = (
        fraction_completed
        * first_total_years
    )

    remaining_years = (
        first_total_years
        - elapsed_years
    )

    # First Mahadasha starts before birth.
    first_start = (
        birth_local
        - datetime.timedelta(
            days=(
                elapsed_years
                * YEAR_DAYS
            )
        )
    )

    periods = []

    current = first_start

    first_index = DASHA_LORDS.index(
        first_lord
    )

    for i in range(9):

        lord = DASHA_LORDS[
            (first_index + i) % 9
        ]

        if i == 0:

            duration_years = (
                remaining_years
            )

        else:

            duration_years = (
                DASHA_YEARS[lord]
            )

        end = add_years(
            current,
            duration_years
        )

        antardasha = (
            calculate_antardasha(
                lord,
                current,
                end
            )
        )

        periods.append({
            "lord": lord,
            "start": current.isoformat(),
            "end": end.isoformat(),
            "years": duration_years,
            "antardasha": antardasha,
        })

        current = end

    return {
        "system": "Vimshottari",

        "total_years": 120,

        "starting_lord": first_lord,

        "mahadasha": periods,
    }


# =========================================================
# MAIN KUNDLI CALCULATION
# =========================================================

def calculate_kundli(
    payload
):

    # -----------------------------------------------------
    # INPUT
    # -----------------------------------------------------

    date_string = str(
        payload.get(
            "date",
            ""
        )
    ).strip()

    time_string = str(
        payload.get(
            "time",
            ""
        )
    ).strip()

    if not date_string:
        raise ValueError(
            "Birth date is required."
        )

    if not time_string:
        raise ValueError(
            "Birth time is required."
        )

    try:

        latitude = float(
            payload.get("lat")
        )

        longitude = float(
            payload.get("lon")
        )

    except Exception:

        raise ValueError(
            "Valid latitude and longitude are required."
        )

    if not -90 <= latitude <= 90:

        raise ValueError(
            "Latitude must be between -90 and 90."
        )

    if not -180 <= longitude <= 180:

        raise ValueError(
            "Longitude must be between -180 and 180."
        )

    timezone_name = (
        payload.get("timezone")
        or "Asia/Kolkata"
    )

    # -----------------------------------------------------
    # DATE / TIME
    # -----------------------------------------------------

    try:

        birth_date = (
            datetime.date.fromisoformat(
                date_string
            )
        )

        birth_time = (
            datetime.time.fromisoformat(
                time_string
            )
        )

    except Exception:

        raise ValueError(
            "Invalid date or time format."
        )

    try:

        tz = zoneinfo.ZoneInfo(
            timezone_name
        )

    except Exception:

        timezone_name = "Asia/Kolkata"

        tz = zoneinfo.ZoneInfo(
            timezone_name
        )

    birth_local = (
        datetime.datetime.combine(
            birth_date,
            birth_time
        ).replace(
            tzinfo=tz
        )
    )

    birth_utc = (
        birth_local.astimezone(
            datetime.timezone.utc
        )
    )

    # -----------------------------------------------------
    # JULIAN DAY
    # -----------------------------------------------------

    decimal_hour = (
        birth_utc.hour
        + birth_utc.minute / 60.0
        + birth_utc.second / 3600.0
        + birth_utc.microsecond
        / 3600000000.0
    )

    jd = swe.julday(
        birth_utc.year,
        birth_utc.month,
        birth_utc.day,
        decimal_hour
    )

    # -----------------------------------------------------
    # SWISS FLAGS
    # -----------------------------------------------------

    flags = (
        swe.FLG_SWIEPH
        | swe.FLG_SIDEREAL
    )

    # -----------------------------------------------------
    # HOUSES
    # -----------------------------------------------------

    house_data = calculate_houses(
        jd,
        latitude,
        longitude
    )

    ascendant = (
        house_data["ascendant"]
    )

    asc_sign = sign_index(
        ascendant
    )

    # -----------------------------------------------------
    # PLANETS
    # -----------------------------------------------------

    planets = []

    for name, planet_id in PLANETS.items():

        xx = planet_result(
            jd,
            planet_id,
            flags
        )

        if xx is None or len(xx) < 1:

            raise RuntimeError(
                "Swiss Ephemeris returned no data for "
                + name
            )

        longitude_sidereal = norm360(
            float(xx[0])
        )

        sign = sign_index(
            longitude_sidereal
        )

        degree = (
            longitude_sidereal
            % 30
        )

        house = (
            (sign - asc_sign)
            % 12
        ) + 1

        planets.append({
            "name": name,
            "longitude": longitude_sidereal,
            "sign": sign,
            "sign_name": SIGNS[sign],
            "degree": degree,
            "house": house,
        })

    # -----------------------------------------------------
    # KETU
    # -----------------------------------------------------

    rahu = next(
        p for p in planets
        if p["name"] == "Rahu"
    )

    ketu_longitude = norm360(
        rahu["longitude"]
        + 180.0
    )

    ketu_sign = sign_index(
        ketu_longitude
    )

    ketu_degree = (
        ketu_longitude
        % 30
    )

    ketu_house = (
        (ketu_sign - asc_sign)
        % 12
    ) + 1

    planets.append({
        "name": "Ketu",
        "longitude": ketu_longitude,
        "sign": ketu_sign,
        "sign_name": SIGNS[ketu_sign],
        "degree": ketu_degree,
        "house": ketu_house,
    })

    # -----------------------------------------------------
    # MOON
    # -----------------------------------------------------

    moon = next(
        p for p in planets
        if p["name"] == "Moon"
    )

    # -----------------------------------------------------
    # NAKSHATRA
    # -----------------------------------------------------

    nakshatra = (
        calculate_nakshatra(
            moon["longitude"]
        )
    )

    # -----------------------------------------------------
    # D9
    # -----------------------------------------------------

    d9_planets = []

    for planet in planets:

        d9_planets.append(
            calculate_navamsa(
                planet
            )
        )

    # -----------------------------------------------------
    # VIMSHOTTARI
    # -----------------------------------------------------

    vimshottari = (
        calculate_vimshottari(
            moon["longitude"],
            birth_local
        )
    )

    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return {

        "success": True,

        "input": {
            "name": payload.get(
                "name",
                ""
            ),

            "date": date_string,

            "time": time_string,

            "place": payload.get(
                "place",
                ""
            ),

            "lat": latitude,

            "lon": longitude,

            "timezone": timezone_name,
        },

        "astronomy": {

            "julian_day_ut": jd,

            "ayanamsha": (
                house_data[
                    "ayanamsha"
                ]
            ),

            "ayanamsha_system": "Lahiri",
        },

        "lagna": {

            "longitude": ascendant,

            "sign": asc_sign,

            "sign_name": SIGNS[
                asc_sign
            ],

            "degree": (
                ascendant % 30
            ),
        },

        "planets": planets,

        "nakshatra": nakshatra,

        "d9": {

            "name": "Navamsa",

            "planets": d9_planets,
        },

        "vimshottari": vimshottari,
    }


# =========================================================
# VERCEL HTTP HANDLER
# =========================================================

class handler(
    BaseHTTPRequestHandler
):

    def send_json(
        self,
        status,
        data
    ):

        body = json.dumps(
            data,
            ensure_ascii=False,
            default=str
        ).encode(
            "utf-8"
        )

        self.send_response(
            status
        )

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.end_headers()

        self.wfile.write(
            body
        )

    # -----------------------------------------------------
    # OPTIONS
    # -----------------------------------------------------

    def do_OPTIONS(self):

        self.send_response(
            204
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    def do_POST(self):

        try:

            content_length = int(
                self.headers.get(
                    "content-length",
                    "0"
                )
            )

            raw_body = (
                self.rfile.read(
                    content_length
                )
            )

            if not raw_body:

                raise ValueError(
                    "Request body is empty."
                )

            payload = json.loads(
                raw_body.decode(
                    "utf-8"
                )
            )

            result = (
                calculate_kundli(
                    payload
                )
            )

            self.send_json(
                200,
                result
            )

        except Exception as error:

            self.send_json(
                400,
                {
                    "success": False,

                    "error": str(error),

                    "error_type": (
                        type(error).__name__
                    ),
                }
            )
