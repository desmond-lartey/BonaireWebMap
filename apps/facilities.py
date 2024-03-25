# apps/facilities.py
import streamlit as st
import geemap.foliumap as geemap
import geopandas as gpd
import os

def app():
    st.title("Facilities and Land Uses")

    # Sidebar for base map selection using geemap's basemaps
    basemap_choice = st.sidebar.selectbox(
        "Choose a basemap:",
        list(geemap.basemaps.keys()),
        index=list(geemap.basemaps.keys()).index("HYBRID")  # Default to HYBRID for a nice satellite and streets mix
    )

    # Initialize the map with the selected basemap
    m = geemap.Map(center=[12.15, -68.27], zoom=11, basemap=geemap.basemaps[basemap_choice])

    # Function to add a shapefile layer
    def add_shapefile_layer(shapefile_path, layer_name):
        # Read the shapefile
        gdf = gpd.read_file(shapefile_path)
        
        # Add the GeoDataFrame to the map
        m.add_gdf(gdf, layer_name=layer_name)

    # Dynamically construct the path to the shapefile and add it as a layer
    # This assumes your Streamlit app runs from the root of your project
    shapefile_path = os.path.join("newlyexportedshp", "bonaireboundary.shp")
    add_shapefile_layer(shapefile_path, "Bonaire Boundary")

    # Display the map
    m.to_streamlit(height=700)
