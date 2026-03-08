import requests
from skyfield.api import EarthSatellite, load

# Simple fallback TLE for ISS if live download fails
FALLBACK_TLES = {
    25544: (
        "ISS (ZARYA)",
        "1 25544U 98067A   24067.51782528  .00016717  00000+0  10270-3 0  9996",
        "2 25544  51.6416 205.1232 0006157  75.4340  31.2935 15.50008819442859",
    ),
    20580: (
        "HST",
        "1 20580U 90037B   24067.19947312  .00000816  00000+0  38531-4 0  9997",
        "2 20580  28.4690 130.5360 0002873  53.9958 306.1152 15.25536607764512",
    ),
    25338: (
        "NOAA 15",
        "1 25338U 98030A   24067.47820112  .00000092  00000+0  79674-4 0  9994",
        "2 25338  98.7391 133.7275 0011399 357.6890   2.4250 14.26088727340624",
    ),
}


def fetch_tle_by_catnr(catnr):
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={catnr}&FORMAT=TLE"
    ts = load.timescale()

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        lines = [line.strip() for line in response.text.strip().splitlines() if line.strip()]

        if len(lines) < 3:
            raise ValueError("Could not retrieve valid TLE data.")

        name = lines[0]
        line1 = lines[1]
        line2 = lines[2]

        return EarthSatellite(line1, line2, name, ts)

    except Exception:
        if catnr in FALLBACK_TLES:
            name, line1, line2 = FALLBACK_TLES[catnr]
            return EarthSatellite(line1, line2, name, ts)
        raise


def get_default_satellite():
    return fetch_tle_by_catnr(25544)