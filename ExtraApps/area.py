import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import folium
from streamlit_folium import folium_static
import os

def read_and_prepare_data(excel_file_path):
    if not os.path.exists(excel_file_path):
        st.error(f"Excel file not found at {excel_file_path}")
        return None
    
    # Read the Excel file
    df = pd.read_excel(excel_file_path)
    
    # Convert DataFrame to GeoDataFrame by creating polygons from the bounding box columns
    gdf = gpd.GeoDataFrame(df, geometry=df.apply(lambda row: box(row['left'], row['bottom'], row['right'], row['top']), axis=1))
    
    return gdf

def add_hexagons_to_map(gdf, m):
    # Add hexagons to the map as clickable polygons
    for _, row in gdf.iterrows():
        # Create a popup with the desired information (adjust as needed)
        popup_content = f"ID: {row['id']}<br>Population Sum: {row['sum']}"  # Adjust 'sum' as per your column
        popup = folium.Popup(popup_content, max_width=300)
        
        # Add polygon to the map
        folium.GeoJson(row['geometry'], popup=popup).add_to(m)

def app():
    st.title("Population Analysis - Hexagon Visualization")

    # Dynamically construct the path to the Excel file
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    excel_file_path = os.path.join(project_root, "newlyexportedshp", "zonalstats.xlsx")

    # Read and prepare data
    gdf = read_and_prepare_data(excel_file_path)
    
    if gdf is not None:
        # Initialize a folium map centered on Bonaire (adjust the location as needed)
        m = folium.Map(location=[12.15, -68.27], zoom_start=11)
        
        # Add hexagons to the map
        add_hexagons_to_map(gdf, m)
        
        # Display the map in Streamlit
        folium_static(m)

        # Here, you can add additional code for interactive plots based on gdf

if __name__ == "__main__":
    app()
