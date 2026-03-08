from skyfield.api import wgs84, load


class SatelliteTracker:
    def __init__(self, satellite, latitude, longitude, elevation_m=0):
        self.satellite = satellite
        self.location = wgs84.latlon(
            latitude_degrees=latitude,
            longitude_degrees=longitude,
            elevation_m=elevation_m
        )
        self.ts = load.timescale()

    def get_position(self):
        t = self.ts.now()
        difference = self.satellite - self.location
        topocentric = difference.at(t)

        alt, az, distance = topocentric.altaz()

        return {
            "satellite_name": self.satellite.name,
            "altitude_deg": alt.degrees,
            "azimuth_deg": az.degrees,
            "distance_km": distance.km,
            "is_visible": alt.degrees > 0
        }

    def get_ground_position(self):
        t = self.ts.now()
        geocentric = self.satellite.at(t)
        subpoint = wgs84.subpoint(geocentric)

        return {
            "latitude": subpoint.latitude.degrees,
            "longitude": subpoint.longitude.degrees
        }