# neighborhoods.py
import streamlit as st
from turtle import st
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_zonal_stats(hexgrid_shp_path, population_tif_path):
    # Ensure both shapefile and .tif file paths exist
    if not os.path.exists(hexgrid_shp_path):
        st.error(f"Hexgrid shapefile not found at {hexgrid_shp_path}")
        return None
    if not os.path.exists(population_tif_path):
        st.error(f"Population .tif file not found at {population_tif_path}")
        return None
    
    # Load the hexgrid shapefile
    hexgrids = gpd.read_file(hexgrid_shp_path)

    # Calculate zonal statistics
    stats = zonal_stats(hexgrid_shp_path, population_tif_path, stats="sum", all_touched=True)

    # Add population data to hexgrids GeoDataFrame
    hexgrids['population'] = [stat['sum'] for stat in stats]
    
    # Assuming the area of hexgrids is in square meters, calculate population density
    hexgrids['pop_density'] = hexgrids['population'] / hexgrids.geometry.area * 1000000  # for density per sq km

    return hexgrids

def plot_population_density(hexgrids):
    # Assuming 'pop_density' is in people per sq km
    hexgrids.plot(column='pop_density', legend=True, cmap='OrRd')
    plt.title("Population Density per Neighborhood")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    return plt

def app():
    st.title("Population Analysis")

    # Dynamically construct the path to the shapefile and .tif file
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    hexgrid_shp_path = os.path.join(project_root, "data", "bonairehexgrid.shp")
    population_tif_path = os.path.join(project_root, "data", "population.tif")

    # Run analysis
    hexgrids = calculate_zonal_stats(hexgrid_shp_path, population_tif_path)
    if hexgrids is not None:
        # Show DataFrame in Streamlit
        st.write(hexgrids[['population', 'pop_density']])

        # Generate plot and show in Streamlit
        fig = plot_population_density(hexgrids)
        st.pyplot(fig)
