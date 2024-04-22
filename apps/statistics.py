#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np  # Import numpy for numerical operations

def load_data(filename):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    data_path = os.path.join(project_root, "newlyexportedshp", filename)
    if os.path.exists(data_path):
        data = pd.read_excel(data_path)
        return data
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()

def convert_categorical_to_numeric(data):
    mappings = {
        'Timeofday': {'Morning': 1, 'Afternoon': 2, 'Evening': 3},
        'Gender': {'Male': 1, 'Female': 2, 'Prefer not to say': 3},
        'Agegroup': {'Infant': 1, 'Child': 2, 'Teen': 3, 'Adult': 4, 'Older adults': 5},
        'Ethnicity': {'White': 1, 'Non-white': 2},
        'Activitytype': {'Cycling': 1, 'Sedentary': 2, 'Dog-walking': 3, 'Walking': 4, 'Scooter/other form of mobility': 5}
    }
    for column, mapping in mappings.items():
        if column in data.columns:
            data[column] = data[column].map(mapping)
    return data

def plot_analysis(data, question):
    sns.set(style="whitegrid")
    if "Correlation Analysis" in question:
        numerical_data = data.select_dtypes(include=[np.number])
        if numerical_data.shape[1] > 1:
            plt.figure(figsize=(10, 8))
            sns.heatmap(numerical_data.corr(), annot=True, cmap='coolwarm')
            plt.title('Correlation Matrix')
            st.pyplot(plt)
        else:
            st.write("Not enough numerical columns for correlation analysis.")

    elif "Distribution Analysis" in question:
        num_cols = data.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            fig, axes = plt.subplots(1, len(num_cols), figsize=(5 * len(num_cols), 4))
            for i, col in enumerate(num_cols):
                sns.histplot(data[col], kde=True, ax=axes[i])
                axes[i].set_title(f'Distribution of {col}')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.write("No numerical columns available for distribution analysis.")

    else:
        fig, axes = plt.subplots(2, 2, figsize=(14, 18))
        color_palette = ["Set2", "Set3", "Pastel1", "Pastel2"]
        # Further details for handling specific cases can be added here
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
        'Observations': ["Demographic Distributions", "Activity Analysis", "Correlation Analysis", "Distribution Analysis"],
        'Survey': ["Travel Mode Analysis", "Vehicle Use Patterns", "Correlation Analysis", "Distribution Analysis"]
    }

    selected_question = st.sidebar.selectbox("Select a question:", questions[dataset_choice])
    plot_analysis(data, selected_question)  # Automatically plot when a question is selected

if __name__ == "__main__":
    app()
