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
    fig, axes = plt.subplots(2, 2, figsize=(14, 18))  # A 2x2 grid for multiple visualizations
    
    if "Correlation Analysis" in question:
        numerical_data = data.select_dtypes(include=[np.number])
        if numerical_data.shape[1] > 1:
            sns.heatmap(numerical_data.corr(), annot=True, cmap='coolwarm', ax=axes[0, 0])
            axes[0, 0].set_title('Correlation Matrix')
            # Hide other plots if not relevant
            for i in range(1, 4):
                axes.flat[i].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            return
        else:
            st.write("Not enough numerical columns for correlation analysis.")
            return

    if "Distribution Analysis" in question:
        num_cols = data.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            for i, col in enumerate(num_cols):
                sns.histplot(data[col], kde=True, ax=axes.flat[i])
                axes.flat[i].set_title(f'Distribution of {col}')
            for i in range(len(num_cols), 4):
                axes.flat[i].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            return
        else:
            st.write("No numerical columns available for distribution analysis.")
            return

    # Implement other types of analyses
    if question == "Demographic Distributions":
        sns.countplot(data=data, x='Gender', ax=axes[0, 0], palette=color_palette[0])
        axes[0, 0].set_title('Gender Distribution')

        sns.countplot(data=data, x='Agegroup', ax=axes[0, 1], palette=color_palette[1])
        axes[0, 1].set_title('Age Group Distribution')
        axes[0, 1].tick_params(axis='x', rotation=45)

        sns.countplot(data=data, x='Ethnicity', ax=axes[1, 0], palette=color_palette[2])
        axes[1, 0].set_title('Ethnicity Distribution')
        axes[1, 0].tick_params(axis='x', rotation=45)

        sns.countplot(data=data, x='Activitytype', ax=axes[1, 1], palette=color_palette[3])
        axes[1, 1].set_title('Activity Type Distribution')
        axes[1, 1].tick_params(axis='x', rotation=45)

    elif question == "Travel Mode Analysis":
        travel_mode_crosstab = pd.crosstab(data['Agegroup'], data['Travel'])
        sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="viridis", ax=axes[0, 0])
        axes[0, 0].set_title('Travel Mode by Age Group')

        sns.countplot(data=data, x='Travel', ax=axes[0, 1], palette=color_palette[1])
        axes[0, 1].set_title('Travel Mode Preferences')
        axes[0, 1].tick_params(axis='x', rotation=45)

        sns.countplot(data=data, x='Car', ax=axes[1, 0], palette=color_palette[2])
        axes[1, 0].set_title('Car Usage Frequency')
        axes[1, 0].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

def demographic_distributions(data, axes):
    color_palette = ["Set2", "Set3", "Pastel1", "Pastel2"]
    sns.countplot(data=data, x='Gender', ax=axes[0, 0], palette=color_palette[0])
    axes[0, 0].set_title('Gender Distribution')
    sns.countplot(data=data, x='Agegroup', ax=axes[0, 1], palette=color_palette[1])
    axes[0, 1].set_title('Age Group Distribution')
    sns.countplot(data=data, x='Ethnicity', ax=axes[1, 0], palette=color_palette[2])
    axes[1, 0].set_title('Ethnicity Distribution')
    sns.countplot(data=data, x='Activitytype', ax=axes[1, 1], palette=color_palette[3])
    axes[1, 1].set_title('Activity Type Distribution')

def travel_mode_analysis(data, axes):
    travel_mode_crosstab = pd.crosstab(data['Agegroup'], data['Travel'])
    sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="viridis", ax=axes[0, 0])
    sns.countplot(data=data, x='Travel', ax=axes[0, 1])
    sns.countplot(data=data, x='Car', ax=axes[1, 0])
    axes[0, 1].tick_params(axis='x', rotation=45)

def app():
    st.title("Active Mobility Data Analysis")
    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')
    observations_data = convert_categorical_to_numeric(observations_data)

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
