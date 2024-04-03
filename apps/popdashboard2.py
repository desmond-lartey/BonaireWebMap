import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_data(filename):
    # Dynamically construct the path to the data file
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    data_path = os.path.join(project_root, "newlyexportedshp", filename)  # Path to your data directory

    # Ensure the data file path exists
    if os.path.exists(data_path):
        # Read the CSV data file
        data = pd.read_csv(data_path)
        return data
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found

def app():
    st.title("Population Dashboard")

    # Load the dataset
    data = load_data('HexagonDemographicStatistics_AllBands_CSV.csv')

    if not data.empty:
        # Streamlit app layout
        st.header('Population Distribution Across Neighborhoods')

        # Selecting specific neighborhoods to visualize
        options = st.multiselect('Select Neighborhood IDs', data['id'].unique())
        if options:
            filtered_data = data[data['id'].isin(options)]
            fig = px.bar(filtered_data, x='id', y='_sum', labels={'_sum': 'Population Sum'}, title="Population Sum by Neighborhood")
            st.plotly_chart(fig)
        else:
            st.write("Please select at least one neighborhood to visualize.")
