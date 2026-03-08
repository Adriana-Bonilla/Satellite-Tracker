import requests
from skyfield.api import EarthSatellite, load


def fetch_tle_by_catnr(catnr):
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={catnr}&FORMAT=TLE"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    lines = [line.strip() for line in response.text.strip().splitlines() if line.strip()]

    if len(lines) < 3:
        raise ValueError("Could not retrieve valid TLE data.")

    name = lines[0]
    line1 = lines[1]
    line2 = lines[2]

    ts = load.timescale()
    satellite = EarthSatellite(line1, line2, name, ts)

    return satellite


def get_default_satellite():
    return fetch_tle_by_catnr(25544)