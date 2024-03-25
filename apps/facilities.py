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
        index=list(geemap.basemaps.keys()).index("HYBRID")  # Default to HYBRID
    )

    # Initialize the map with the selected basemap
    #m = geemap.Map(center=[12.15, -68.27], zoom=11, basemap=geemap.basemaps[basemap_choice])
    # Use a known working basemap as a string directly
    m = geemap.Map(center=[12.15, -68.27], zoom=11, basemap='HYBRID')


    # Function to add a shapefile layer
    def add_shapefile_layer(shapefile_path, layer_name):
        # Ensure the shapefile path exists
        if os.path.exists(shapefile_path):
            # Read the shapefile
            gdf = gpd.read_file(shapefile_path)
            
            # Add the GeoDataFrame to the map
            m.add_gdf(gdf, layer_name=layer_name, zoom_to_layer=True)
        else:
            st.error(f"Shapefile not found at {shapefile_path}")

    # Dynamically construct the path to the shapefile
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    shapefile_path = os.path.join(project_root, "newlyexportedshp", "bonaireboundary.shp")
    add_shapefile_layer(shapefile_path, "Bonaire Boundary")

    # Display the map
    m.to_streamlit(height=700)
