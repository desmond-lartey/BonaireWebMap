import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import os

# Set page configuration
st.set_page_config(page_title="Bonaire Population Insights", layout="wide")

# Function to load CSV data
def load_data(file_name):
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, "data", file_name)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        st.error("CSV file not found: " + file_name)
        return pd.DataFrame()

# Function to load GeoJSON data
def load_geodata(file_name):
    base_path = os.path.dirname(__file__)
    geojson_path = os.path.join(base_path, "data", file_name)
    if os.path.exists(geojson_path):
        return gpd.read_file(geojson_path)
    else:
        st.error("GeoJSON file not found: " + file_name)
        return gpd.GeoDataFrame()

# Function to melt the data into a long format
def melt_data(data):
    id_vars = [col for col in data.columns if col not in ['2000', '2005', '2010', '2015', '2020', '2024', '2028', '2038']]
    melted_data = data.melt(id_vars=id_vars, value_vars=['2000', '2005', '2010', '2015', '2020', '2024', '2028', '2038'],
                            var_name='Year', value_name='Population')
    melted_data['Year'] = melted_data['Year'].astype(int)  # Ensure 'Year' is an integer for sorting
    return melted_data

# Main application function
def app():
    st.title("Bonaire Population Dashboard")
    population_data = load_data("NeighborhoodPopulationByYear_CSV.csv")
    geodata = load_geodata("HexagonDemographicStatistics_AllBands1.geojson")

    melted_population_data = melt_data(population_data)  # Melt the data for easier manipulation

    # Sidebar for user inputs
    with st.sidebar:
        st.title("Settings")
        years = sorted(melted_population_data['Year'].unique())
        year_selected = st.selectbox('Select Year', years)
        filtered_data = melted_population_data[melted_population_data['Year'] == year_selected]

    # Display choropleth map if data is available
    if not geodata.empty and not filtered_data.empty:
        st.subheader("Population Choropleth Map")
        merged_data = geodata.merge(filtered_data, left_on='id', right_on='id', how='left')
        fig = px.choropleth(
            merged_data,
            geojson=merged_data.geometry,
            locations=merged_data.index,
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

    # Population scatter plot over time
    st.subheader("Population Over Time")
    scatter_fig = px.scatter(
        melted_population_data,
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
