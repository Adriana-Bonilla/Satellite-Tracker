import streamlit as st
import pandas as pd
from satellites import fetch_tle_by_catnr
from tracker import SatelliteTracker

SATELLITES = {
    "ISS": 25544,
    "Hubble Space Telescope": 20580,
    "NOAA 15": 25338,
}

st.set_page_config(page_title="Satellite Tracker", page_icon="🛰️", layout="wide")

st.title("🛰️ Satellite Tracker")
st.write("Track a satellite from your location.")

satellite_name = st.selectbox("Choose a satellite", list(SATELLITES.keys()))
latitude = st.number_input("Latitude", value=18.2011, format="%.4f")
longitude = st.number_input("Longitude", value=-67.1396, format="%.4f")
elevation_m = st.number_input("Elevation (meters)", value=0)

if st.button("Update Position"):
    try:
        satellite = fetch_tle_by_catnr(SATELLITES[satellite_name])

        tracker = SatelliteTracker(
            satellite=satellite,
            latitude=latitude,
            longitude=longitude,
            elevation_m=elevation_m
        )

        position = tracker.get_position()
        ground = tracker.get_ground_position()

        st.subheader(f"Tracking: {position['satellite_name']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Altitude", f"{position['altitude_deg']:.2f}°")
        col2.metric("Azimuth", f"{position['azimuth_deg']:.2f}°")
        col3.metric("Distance", f"{position['distance_km']:.2f} km")

        if position["is_visible"]:
            st.success("Above the horizon")
        else:
            st.warning("Below the horizon")

        st.write("Satellite ground position:")
        st.write(f"Latitude: {ground['latitude']:.4f}")
        st.write(f"Longitude: {ground['longitude']:.4f}")

        import pandas as pd
        df = pd.DataFrame([{"lat": ground["latitude"], "lon": ground["longitude"]}])
        st.map(df, zoom=1)

    except Exception as e:
        st.error(f"Could not load satellite data: {e}")