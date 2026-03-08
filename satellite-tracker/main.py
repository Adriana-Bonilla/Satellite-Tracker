import time 
from satellites import get_default_satellite 
from tracker import SatelliteTracker

def clear_terminal():
    print("\033[2J\033[H", end="")

def main():
    latitude = 18.2011
    longitude = -67.1396
    elevation_m = 0 

    print("Fetching satellite data...")
    satellite = get_default_satellite()
    tracker = SatelliteTracker(
    satellite=satellite, 
    latitude=latitude, 
    longitude=longitude, 
    elevation_m=elevation_m
    )

    try:
        while True:
            position = tracker.get_position()
            clear_terminal()
            print("=== Satellite Tracker ===")
            print(f"Observer location: ({latitude}, {longitude})")
            print(f"Satellite: {position['satellite_name']}")
            print(f"Altitude: {position['altitude_deg']:.2f}°")
            print(f"Azimuth:  {position['azimuth_deg']:.2f}°")
            print(f"Distance: {position['distance_km']:.2f} km")

            if position["is_visible"]:
                print("Status: Above the horizon and visible!")
            else:
                print("Status: Below the horizon or not visible.")

            print("\nUpdating in 5 seconds...Press Ctrl+C to exit.")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nExiting satellite tracker. Goodbye!")

if __name__ == "__main__":   
    main()