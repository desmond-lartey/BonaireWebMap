import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import os

def app():
    st.title("Population Analysis - Interactive Hexgrids")

    # Dynamically construct the path to the shapefile
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    shapefile_path = os.path.join(project_root, "newlyexportedshp", "zonalstats.shp")
    
    # Load the shapefile
    hexgrids = gpd.read_file(shapefile_path)
    
    # Initialize a folium map centered on Bonaire
    m = folium.Map(location=[12.15, -68.27], zoom_start=11)
    
    # Add hexgrids to the map as clickable polygons
    for _, row in hexgrids.iterrows():
        # Simplify geometry for faster rendering (optional)
        simplified_geom = row.geometry.simplify(0.001, preserve_topology=True)
        # Create a popup with the population 'sum' information
        popup = folium.Popup(f"Population Sum: {row['_sum']}", parse_html=True)
        # Add polygon to the map
        folium.GeoJson(simplified_geom, popup=popup).add_to(m)

    # Display the map in Streamlit
    folium_static(m)
