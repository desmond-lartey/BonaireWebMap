import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import os
import numpy as np

# Configuration and data loading
st.set_page_config(page_title="Bonaire Population Insights", layout="wide")

def load_data(file_name):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    file_path = os.path.join(project_root, "data", file_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error("File not found: " + file_name)
        return pd.DataFrame()

def load_geodata(file_name):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    file_path = os.path.join(project_root, "data", file_name)
    if os.path.exists(file_path):
        return gpd.read_file(file_path)
    else:
        st.error("GeoJSON file not found: " + file_name)
        return gpd.GeoDataFrame()

# Main app
def app():
    st.title("Bonaire Population Dashboard")
    population_data = load_data("NeighborhoodPopulationByYear_CSV.csv")
    geodata = load_geodata("bonaire_geo.json")

    # Sidebar
    with st.sidebar:
        st.title("Settings")
        years = population_data['Year'].unique()
        year_selected = st.selectbox('Select Year', sorted(years))
        filtered_data = population_data[population_data['Year'] == year_selected]

    # Choropleth map
    if not geodata.empty and not filtered_data.empty:
        st.subheader("Population Choropleth Map")
        geodata = geodata.merge(filtered_data, on='id', how='left')
        fig = px.choropleth(
            geodata,
            geojson=geodata.geometry,
            locations=geodata.index,
            color="Population",
            color_continuous_scale="Viridis",
            projection="mercator"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
        st.plotly_chart(fig, use_container_width=True)

    # Population treemap
    st.subheader("Population Treemap")
    treemap_fig = px.treemap(
        filtered_data,
        path=['id', 'Year'],
        values='Population',
        color='Population',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(treemap_fig, use_container_width=True)

    # Population scatter plot
    st.subheader("Population Over Time")
    scatter_fig = px.scatter(
        population_data,
        x="Year",
        y="Population",
        size="Population",
        color="Population",
        hover_name="id",
        size_max=60
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

if __name__ == '__main__':
    app()
