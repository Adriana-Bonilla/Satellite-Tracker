import streamlit as st
from satellites import fetch_tle_by_catnr
from tracker import SatelliteTracker


SATELLITES = {
    "ISS": 25544,
    "Hubble Space Telescope": 20580,
    "NOAA 15": 25338,
}

st.set_page_config(page_title="Satellite Tracker", page_icon="🛰️", layout="centered")

st.title("🛰️ Satellite Tracker")
st.write("Track a satellite from your location.")

satellite_name = st.selectbox("Choose a satellite", list(SATELLITES.keys()))
latitude = st.number_input("Latitude", value=18.2011, format="%.4f")
longitude = st.number_input("Longitude", value=-67.1396, format="%.4f")
elevation_m = st.number_input("Elevation (meters)", value=0)

if st.button("Update Position"):
    satellite = fetch_tle_by_catnr(SATELLITES[satellite_name])
    tracker = SatelliteTracker(
        satellite=satellite,
        latitude=latitude,
        longitude=longitude,
        elevation_m=elevation_m
    )

    position = tracker.get_position()

    st.subheader(f"Tracking: {position['satellite_name']}")
    st.metric("Altitude", f"{position['altitude_deg']:.2f}°")
    st.metric("Azimuth", f"{position['azimuth_deg']:.2f}°")
    st.metric("Distance", f"{position['distance_km']:.2f} km")

    if position["is_visible"]:
        st.success("Above the horizon")
    else:
        st.warning("Below the horizon")