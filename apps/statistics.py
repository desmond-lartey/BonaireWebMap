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
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))  # Create a 2x2 grid of plots

    # Different types of analyses and plots depending on the question
    if question == "Activity Type Distribution":
        sns.countplot(data=data, x='Activitytype', ax=axes[0, 0])
        axes[0, 0].set_title('Activity Type Distribution')
        axes[0, 0].tick_params(axis='x', rotation=45)

        sns.boxplot(data=data, x='Activitytype', y='Income', ax=axes[0, 1])
        axes[0, 1].set_title('Income by Activity Type')

        data['Activitytype'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=axes[1, 0])
        axes[1, 0].set_ylabel('')
        axes[1, 0].set_title('Activity Type Pie Chart')

        sns.violinplot(data=data, x='Activitytype', y='Household', ax=axes[1, 1])
        axes[1, 1].set_title('Household Size by Activity Type')

    plt.tight_layout()
    st.pyplot(fig)

def app():
    st.title("Active Mobility Data Analysis")

    # Load Data
    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')

    # Sidebar for user interaction
    st.sidebar.title("User Selection")
    dataset_choice = st.sidebar.radio("Choose the dataset:", ('Observations', 'Survey'))
    data = observations_data if dataset_choice == 'Observations' else survey_data

    if st.sidebar.checkbox("Show Data"):
        st.write(data)

    # Define questions based on the selected dataset
    questions = {
        'Observations': ["Activity Type Distribution", "Gender Distribution", "Peak Activity Times"],
        'Survey': ["Travel Mode Preferences", "Income Distribution", "Household Size Analysis"]
    }

    selected_question = st.sidebar.selectbox("Select a question:", questions[dataset_choice])

    # Choose type of analysis
    analysis_type = st.sidebar.radio("Choose the type of analysis:", ("Descriptive", "Predictive"))

    if analysis_type == "Descriptive":
        if st.sidebar.button("Analyze"):
            plot_analysis(data, selected_question)

    # Predictive Analysis Example
    elif analysis_type == "Predictive":
        st.subheader("Predictive Model Results")
        if st.sidebar.button("Model"):
            st.write("Predictive Model would be implemented here")

    
if __name__ == "__main__":
    app()
