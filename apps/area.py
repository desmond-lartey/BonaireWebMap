# neighborhoods.py
import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import numpy as np
from sklearn.cluster import KMeans
import os


def create_neighborhoods(buildings_gdf, n_neighborhoods):
    # Assuming buildings_gdf has 'geometry' with building locations
    # Convert building points to coordinates array for clustering
    building_coords = np.array(list(buildings_gdf.geometry.apply(lambda x: (x.x, x.y))))
    
    # Use a clustering algorithm like K-Means to group buildings
    kmeans = KMeans(n_clusters=n_neighborhoods)
    buildings_gdf['cluster'] = kmeans.fit_predict(building_coords)
    
    # Create polygons (buffers) around the clusters of buildings for initial neighborhood boundaries
    # Here you may need more sophisticated GIS operations to generate meaningful neighborhoods
    neighborhoods_gdf = buildings_gdf.dissolve(by='cluster', aggfunc='first').buffer(0.01)  # Example buffer, adjust as needed
    
    # Convert buffer polygons to a GeoDataFrame
    neighborhoods_gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(neighborhoods_gdf), crs=buildings_gdf.crs)
    
    return neighborhoods_gdf

def app():
    st.title("Neighborhoods of Bonaire")

    # Initialize a map centered on Bonaire
    m = folium.Map(location=[12.15, -68.27], zoom_start=11)

    # Load geographic data
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    buildings_gdf = os.path.join(project_root, "neighbourhood", "roads.shp")
    add_shapefile_layer(buildings_gdf, "Bonaire Buildings")

    # base_path = os.path.dirname(__file__)  # Directory of this script
    # project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    # shapefile_path = os.path.join(project_root, "newlyexportedshp", "bonaireboundary.shp")
    # add_shapefile_layer(shapefile_path, "Bonaire Boundary")

    # Call the function to create neighborhoods
    neighborhoods_gdf = create_neighborhoods(buildings_gdf, n_neighborhoods=15)


    # Add the neighborhoods to the map
    folium.GeoJson(neighborhoods_gdf, name="Neighborhoods").add_to(m)

    # Display the map in Streamlit
    folium_static(m)


# Remember to include this module in your main.py or wherever you're aggregating your app modules.