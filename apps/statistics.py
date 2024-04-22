#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import streamlit as st

def load_data(filename):
    # Dynamically construct the path to the data file
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    data_path = os.path.join(project_root, "newlyexportedshp", filename)

    # Ensure the data file path exists
    if os.path.exists(data_path):
        # Read the Excel data file
        return pd.read_excel(data_path)
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()

def app():
    st.title("Active Mobility Data Analysis")

    # Load Data
    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')

    # Sidebar for user interaction
    st.sidebar.title("User Selection")

    # Select dataset
    dataset_choice = st.sidebar.radio("Choose the dataset:", ('Observations', 'Survey'))
    data = observations_data if dataset_choice == 'Observations' else survey_data

    # Display data
    if st.sidebar.checkbox("Show Data"):
        st.write(data)

    # Assuming a common column 'Category' exists or handling the case when it does not
    if 'Category' in data.columns:
        categories = data['Category'].unique().tolist()
        selected_category = st.sidebar.selectbox("Select a category:", categories)
    else:
        st.write("No 'Category' column found in the dataset.")

    # Select type of analysis
    analysis_type = st.sidebar.radio("Choose the type of analysis:", ("Descriptive", "Predictive"))
    
    # Descriptive Analysis Example
    if analysis_type == "Descriptive":
        st.subheader("Descriptive Statistics")
        if st.sidebar.button("Generate"):
            st.write(data.describe())

    # Predictive Analysis Example
    elif analysis_type == "Predictive":
        st.subheader("Predictive Model Results")
        if st.sidebar.button("Model"):
            # Dummy placeholder for predictive analysis
            st.write("Predictive Model would be implemented here")

    # Footer with contact information and additional resources
    st.sidebar.markdown("### Contact Information")
    st.sidebar.info("This web app is maintained by [Your Name]. For any issues or suggestions, contact us via [Email](mailto:your_email@example.com).")

# Ensures that this script can be run as a standalone app in Streamlit
if __name__ == "__main__":
    app()
