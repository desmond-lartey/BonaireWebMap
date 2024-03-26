# neighborhoods.py
import os
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import streamlit as st

def app():
    st.title("Neighborhoods of Bonaire")

    # Initialize a map centered on Bonaire
    m = folium.Map(location=[12.15, -68.27], zoom_start=11)

    # Function to add a shapefile layer
    def add_shapefile_layer(shapefile_path, layer_name, style=None):
        # Ensure the shapefile path exists
        if os.path.exists(shapefile_path):
            # Read the shapefile
            gdf = gpd.read_file(shapefile_path)
            
            # Add the GeoDataFrame to the map as a GeoJson layer
            folium.GeoJson(
                gdf,
                name=layer_name,
                style_function=lambda x: style if style else {'color': 'blue', 'weight': 3}
            ).add_to(m)
        else:
            st.error(f"Shapefile not found at {shapefile_path}")

    # Construct the path to the shapefiles
    base_path = os.path.dirname(__file__)  # Directory of this script
    boundary_path = os.path.join(base_path, "bonaireboundary.shp")
    roads_path = os.path.join(base_path, "highways.shp")
    buildings_path = os.path.join(base_path, "buildings2.shp")

    # Add each layer to the map
    add_shapefile_layer(boundary_path, "Bonaire Boundary")
    add_shapefile_layer(roads_path, "Roads", style={'color': 'grey', 'weight': 1})
    add_shapefile_layer(buildings_path, "Buildings", style={'color': 'black', 'weight': 1})

    # Display the map in Streamlit
    folium_static(m)

# Rest of your Streamlit code below (e.g., if __name__ == "__main__":)
