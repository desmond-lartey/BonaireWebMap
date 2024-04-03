import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_data(filename):
    # Dynamically construct the path to the data file
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    data_path = os.path.join(project_root, "newlyexportedshp", filename)

    # Ensure the data file path exists
    if os.path.exists(data_path):
        # Read the CSV data file
        return pd.read_csv(data_path)
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()

def app():
    st.title("Population Dashboard")

    # Load the dataset
    data = load_data('HexagonDemographicStatistics_AllBands_CSV.csv')

    if not data.empty:
        # Apply a threshold to filter out neighborhoods with insignificant populations for clarity in visualization
        threshold = st.slider('Population Sum Threshold for Visualization', min_value=10, max_value=2000, value=10, step=10)
        significant_data = data[data['_sum'] > threshold]

        # Display Overall Population Distribution Across All Significant Neighborhoods
        st.header('Overall Population Distribution Across Neighborhoods')
        fig_overall = px.bar(significant_data, x='id', y='_sum', labels={'_sum': 'Population Sum'}, title="Population Sum by Neighborhood")
        st.plotly_chart(fig_overall)

        # Interactive Gender and Age Cohort Distribution Visualizations
        st.header('Detailed Gender and Age Cohort Distribution')

        # Option to select specific gender for detailed visualization
        gender_option = st.selectbox('Select Gender for Visualization', ['F', 'M'])

        gender_data = significant_data[[col for col in significant_data.columns if col.startswith(gender_option)] + ['id']]
        # Melt the dataframe for better visualization handling
        gender_data = gender_data.melt(id_vars=['id'], var_name='Age Cohort', value_name='Population')
        # Improve readability of age cohorts in the visualization
        gender_data['Age Cohort'] = gender_data['Age Cohort'].apply(lambda x: x.replace(gender_option + '_', '') + ' years (' + gender_option + ')')
        # Generate and display the Plotly bar chart for selected gender
        fig_gender_age = px.bar(gender_data, x='id', y='Population', color='Age Cohort', title=f"Population by Age Cohort for {gender_option} across Neighborhoods")
        st.plotly_chart(fig_gender_age)

        # Additional visualizations for deeper insights into the data can be added here
        # Examples: Age cohort comparison within each gender, neighborhood comparisons, etc.

if __name__ == "__main__":
    app()
