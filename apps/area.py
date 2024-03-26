# neighborhoods.py
import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.geometry import Point, Polygon

def app():
    st.title("Neighborhoods of Bonaire")

    # Initialize a map centered on Bonaire
    m = folium.Map(location=[12.15, -68.27], zoom_start=11)

    # Example list of neighborhoods with manually approximated central points (latitude, longitude)
    neighborhoods_info = [
        {"name": "Playa", "location": (12.1500, -68.2767)},
        # Add other neighborhoods with their approximate central locations
    ]

    # Creating approximate neighborhood boundaries (e.g., circles with a radius of 500 meters)
    for neighborhood in neighborhoods_info:
        # Creating a point for the neighborhood center
        center_point = Point(neighborhood["location"][1], neighborhood["location"][0])
        # Buffering the point to create an approximate area (polygon)
        area = center_point.buffer(0.005)  # Adjust the buffer size as necessary
        
        # Adding the buffered area as a polygon to the map
        folium.GeoJson(area, tooltip=neighborhood["name"]).add_to(m)

    # Display the map in Streamlit
    folium_static(m)

# Remember to include this module in your main.py or wherever you're aggregating your app modules.
