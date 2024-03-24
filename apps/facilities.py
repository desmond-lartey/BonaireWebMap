# apps/facilities.py
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import json

def app():
    st.title("Facilities and Land Uses")

    # Sidebar for base map selection
    basemap_choice = st.sidebar.radio(
        "Choose a basemap",
        ("OpenStreetMap", "HYBRID", "TERRAIN", "ESRI Satellite"),  # Add more basemap options here
        index=0  # Default to OpenStreetMap
    )

    # Initialize the map without specifying center and zoom here
    m = leafmap.Map()

    # Function to add a shapefile layer
    def add_shapefile_layer(shapefile_path, layer_name):
        # Read the shapefile
        gdf = gpd.read_file(shapefile_path)

        # Convert GeoDataFrame to GeoJSON
        geojson = json.loads(gdf.to_json())

        # Add the GeoJSON to the map
        m.add_geojson(geojson, layer_name=layer_name)

    # Example of adding a shapefile layer
    shapefile_path = r"C:\Users\Gebruiker\Desktop\My Lab\Bonaire\BonaireWebMap\data\newlyexportedshp\bonaireboundary.shp"
    add_shapefile_layer(shapefile_path, "Bonaire Boundary")

    # After adding layers, manually adjust the view.
    m.set_center(lon=-68.27, lat=12.15, zoom=10)

    # Set the basemap (Leafmap uses the basemap after adding layers)
    m.set_basemap(basemap_choice)

    # Display the map
    m.to_streamlit(height=700)
