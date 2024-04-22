#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_data(filename):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    data_path = os.path.join(project_root, "newlyexportedshp", filename)
    if os.path.exists(data_path):
        return pd.read_excel(data_path)
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()

def plot_analysis(data, question):
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 18))  # A 2x2 grid for multiple visualizations

    if question == "Demographic Distributions":
        sns.countplot(data=data, x='Gender', ax=axes[0, 0])
        axes[0, 0].set_title('Gender Distribution')

        sns.countplot(data=data, x='Age', ax=axes[0, 1])
        axes[0, 1].set_title('Age Group Distribution')
        axes[0, 1].tick_params(axis='x', rotation=45)

        sns.countplot(data=data, x='Ethnicity', ax=axes[1, 0])
        axes[1, 0].set_title('Ethnicity Distribution')
        axes[1, 0].tick_params(axis='x', rotation=45)

        sns.countplot(data=data, x='Activitytype', ax=axes[1, 1])
        axes[1, 1].set_title('Activity Type Distribution')
        axes[1, 1].tick_params(axis='x', rotation=45)

    elif question == "Travel Mode Analysis":
        travel_mode_crosstab = pd.crosstab(data['Age'], data['Travel'])
        sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="Blues", ax=axes[0, 0])
        axes[0, 0].set_title('Travel Mode by Age Group')

        sns.countplot(data=data, x='Travel', ax=axes[0, 1])
        axes[0, 1].set_title('Travel Mode Preferences')
        axes[0, 1].tick_params(axis='x', rotation=45)

        sns.countplot(data=data, x='Car', ax=axes[1, 0])
        axes[1, 0].set_title('Car Usage Frequency')
        axes[1, 0].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

def app():
    st.title("Active Mobility Data Analysis")

    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')

    st.sidebar.title("User Selection")
    dataset_choice = st.sidebar.radio("Choose the dataset:", ('Observations', 'Survey'))
    data = observations_data if dataset_choice == 'Observations' else survey_data

    if st.sidebar.checkbox("Show Data"):
        st.write(data)

    questions = {
        'Observations': ["Demographic Distributions"],
        'Survey': ["Travel Mode Analysis"]
    }

    selected_question = st.sidebar.selectbox("Select a question:", questions[dataset_choice])

    analysis_type = st.sidebar.radio("Choose the type of analysis:", ("Descriptive", "Predictive"))
    if analysis_type == "Descriptive":
        if st.sidebar.button("Analyze"):
            plot_analysis(data, selected_question)

    elif analysis_type == "Predictive":
        st.subheader("Predictive Model Results")
        if st.sidebar.button("Model"):
            st.write("Predictive model would be implemented here")

    
if __name__ == "__main__":
    app()
