import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import os

# Setup page configuration
st.set_page_config(page_title="Bonaire Population Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load geospatial data
def load_geodata(filename):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    geojson_path = os.path.join(project_root, "newlyexportedshp", filename)
    return gpd.read_file(geojson_path) if os.path.exists(geojson_path) else gpd.GeoDataFrame()

# Create choropleth map function
def create_choropleth(geodata, population_data, year):
    # Ensure 'id' columns are the same data type
    geodata['id'] = geodata['id'].astype(str)
    population_data['id'] = population_data['id'].astype(str)

    # Merge the geodata with population data on the 'id' column
    merged_data = geodata.merge(population_data, how='left', on='id')
    merged_data = merged_data[merged_data['Year'] == year]  # Filter data for the selected year
    
    # Creating choropleth map using Plotly
    fig = px.choropleth(
        merged_data,
        geojson=merged_data.geometry,
        locations=merged_data.index,
        color='Population',
        color_continuous_scale="Viridis",
        projection="mercator"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    return fig

# Main app function
def app():
    st.title("Bonaire Population Dashboard")
    
    # Load data
    population_data = pd.read_csv("population_data.csv")
    geodata = load_geodata("bonaire_geo.json")

    # Sidebar for year selection
    with st.sidebar:
        year = st.selectbox("Select Year", options=population_data['Year'].unique(), index=0)
    
    # Display choropleth map
    st.header(f"Population Distribution in {year}")
    choropleth_fig = create_choropleth(geodata, population_data, year)
    st.plotly_chart(choropleth_fig, use_container_width=True)

# Run the app
if __name__ == "__main__":
    app()
