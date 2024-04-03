import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_data(filename):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    data_path = os.path.join(project_root, "newlyexportedshp", filename)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()

def app():
    st.title("Population Dashboard")

    # Load the dataset
    data = load_data('HexagonDemographicStatistics_AllBands_CSV.csv')

    if not data.empty:
        # Filter out neighborhoods with insignificant populations (example threshold: sum of populations < 0.1)
        significant_data = data[data['_sum'] > 10]

        # Overall Population Distribution Across All Significant Neighborhoods
        st.header('Overall Population Distribution Across Neighborhoods')
        fig_overall = px.bar(significant_data, x='id', y='_sum', labels={'_sum': 'Population Sum'}, title="Population Sum by Neighborhood")
        st.plotly_chart(fig_overall)

        # Gender Distribution Across Neighborhoods
        st.header('Gender Distribution Across Neighborhoods')
        gender_columns = [col for col in data.columns if 'F_' in col or 'M_' in col]
        gender_data = significant_data[gender_columns + ['id']].melt(id_vars=['id'], var_name='Gender/Age', value_name='Population')
        fig_gender = px.bar(gender_data, x='id', y='Population', color='Gender/Age', title="Population by Gender and Age Group across Neighborhoods")
        st.plotly_chart(fig_gender)

        # Age Cohorts Distribution
        st.header('Age Cohorts Distribution Across Neighborhoods')
        # You might want to refine this to show specific cohorts or comparisons that are most relevant.
        age_cohorts = [col for col in data.columns if '_' in col and 'sum' in col]
        cohort_data = significant_data[age_cohorts + ['id']].melt(id_vars=['id'], var_name='Age Cohort', value_name='Population')
        fig_cohorts = px.bar(cohort_data, x='id', y='Population', color='Age Cohort', title="Population by Age Cohort across Neighborhoods")
        st.plotly_chart(fig_cohorts)

        # Add more visualizations here as needed

