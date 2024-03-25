# apps/facilities.py
import streamlit as st
from leafmap.foliumap import Map 
import leafmap.foliumap as leafmap
import geopandas as gpd
import json
import os

def app():
    st.title("Facilities and Land Uses")

    # Assuming 'basemap_choice' is obtained from the sidebar selection
    basemap_choice = st.sidebar.radio(
        "Choose a basemap",
        ("OpenStreetMap", "HYBRID", "TERRAIN", "ESRI Satellite"),  # Example options
        index=0
    )

    # Mapping user choice to leafmap basemap constants (this is an example, adjust based on actual basemap options)
    basemap_mapping = {
        "OpenStreetMap": "ROADMAP",
        "HYBRID": "HYBRID",
        "TERRAIN": "TERRAIN",
        "ESRI Satellite": "ESRI"
    }
    
    # Create the Map object with the selected basemap
    m = Map(basemap=basemap_mapping.get(basemap_choice, "OpenStreetMap"))

    # Function to add a shapefile layer
    def add_shapefile_layer(shapefile_path, layer_name):
        # Read the shapefile
        gdf = gpd.read_file(shapefile_path)

        # Convert GeoDataFrame to GeoJSON
        geojson = json.loads(gdf.to_json())

        # Add the GeoJSON to the map
        m.add_geojson(geojson, layer_name=layer_name)

    # Example of adding a shapefile layer
    # shapefile_path = "C:\\Users\\Gebruiker\\Desktop\\My Lab\\Bonaire\\BonaireWebMap\\newlyexportedshp\\bonaireboundary.shp"
    # add_shapefile_layer(shapefile_path, "Bonaire Boundary")

    base_path = os.path.dirname(os.path.dirname(__file__))  # Goes up one directory level from 'apps'
    shapefile_rel_path = os.path.join("newlyexportedshp", "bonaireboundary.shp")
    shapefile_path = os.path.join(base_path, shapefile_rel_path)
    add_shapefile_layer(shapefile_path, "Bonaire Boundary")


    # After adding layers, manually adjust the view.
    m.set_center(lon=-68.27, lat=12.15, zoom=10)

    # Set the basemap (Leafmap uses the basemap after adding layers)
    m.set_basemap(basemap_choice)

    # Display the map
    m.to_streamlit(height=700)
