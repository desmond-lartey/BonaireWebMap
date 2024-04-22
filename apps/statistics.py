#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

def load_data(filename):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    data_path = os.path.join(project_root, "newlyexportedshp", filename)
    if os.path.exists(data_path):
        return pd.read_excel(data_path)
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
    numeric_data = data.copy()
    for column, mapping in mappings.items():
        if column in numeric_data.columns:
            numeric_data[column] = numeric_data[column].map(mapping)
    return numeric_data, data

def plot_analysis(data, question):
    # Direct function call based on question
    if question in analysis_functions:
        analysis_functions[question](data)

def correlation_analysis(data):
    numeric_data = data.select_dtypes(include=[np.number])
    if numeric_data.shape[1] > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        st.pyplot()
    else:
        st.write("Not enough numerical columns for correlation analysis.")

def distribution_analysis(data):
    numeric_data = data.select_dtypes(include=[np.number])
    if not numeric_data.empty:
        fig, axes = plt.subplots(1, len(numeric_data.columns), figsize=(5 * len(numeric_data.columns), 4))
        for i, col in enumerate(numeric_data.columns):
            sns.histplot(numeric_data[col], kde=True, ax=axes[i])
            axes[i].set_title(f'Distribution of {col}')
        plt.tight_layout()
        st.pyplot()
    else:
        st.write("No numerical columns available for distribution analysis.")

def demographic_distributions(data):
    fig, axes = plt.subplots(2, 2, figsize=(14, 18))
    color_palette = ["Set2", "Set3", "Pastel1", "Pastel2"]
    categories = ['Gender', 'Agegroup', 'Ethnicity', 'Activitytype']
    for i, category in enumerate(categories):
        sns.countplot(data=data, x=category, ax=axes[i//2, i%2], palette=color_palette[i%4])
        axes[i//2, i%2].set_title(f'{category} Distribution')
        axes[i//2, i%2].tick_params(axis='x', rotation=45)  # Ensure rotation for better label visibility
    plt.tight_layout()
    st.pyplot()

def travel_mode_analysis(data):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    travel_mode_crosstab = pd.crosstab(data['Agegroup'], data['Travel'])
    sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="viridis", ax=axes[0])
    axes[0].set_title('Travel Mode by Age Group')
    sns.countplot(data=data, x='Travel', ax=axes[1])
    axes[1].set_title('Travel Mode Preferences')
    axes[1].tick_params(axis='x', rotation=45)  # Apply rotation here as well
    plt.tight_layout()
    st.pyplot()

def vehicle_use_patterns(data):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    sns.countplot(data=data, x='Car', ax=axes[0], palette="Set3")
    axes[0].set_title('Car Usage Frequency')
    axes[0].tick_params(axis='x', rotation=45)  # Apply rotation
    sns.countplot(data=data, x='Bicycle', ax=axes[1], palette="Set2")
    axes[1].set_title('Bicycle Usage Frequency')
    axes[1].tick_params(axis='x', rotation=45)  # Apply rotation
    plt.tight_layout()
    st.pyplot()

def activity_analysis(data):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    sns.countplot(data=data, x='Activitytype', ax=axes[0], palette="Pastel1")
    axes[0].set_title('Activity Type Distribution')
    axes[0].tick_params(axis='x', rotation=45)  # Apply rotation
    sns.countplot(data=data, x='Timeofday', ax=axes[1], palette="Pastel2")
    axes[1].set_title('Time of Day Distribution')
    axes[1].tick_params(axis='x', rotation=45)  # Apply rotation
    plt.tight_layout()
    st.pyplot()


def app():
    st.title("Active Mobility Data Analysis")
    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')
    observations_numeric_data, observations_categorical_data = convert_categorical_to_numeric(observations_data)

    st.sidebar.title("User Selection")
    dataset_choice = st.sidebar.radio("Choose the dataset:", ('Observations', 'Survey'))
    data = observations_categorical_data if dataset_choice == 'Observations' else survey_data

    if st.sidebar.checkbox("Show Data"):
        st.write(data)

    questions = {
        'Observations': ["Demographic Distributions", "Activity Analysis", "Correlation Analysis", "Distribution Analysis"],
        'Survey': ["Travel Mode Analysis", "Vehicle Use Patterns", "Correlation Analysis", "Distribution Analysis"]
    }

    selected_question = st.sidebar.selectbox("Select a question:", questions[dataset_choice])
    plot_analysis(data, selected_question)

# Dictionary to map questions to function calls
analysis_functions = {
    "Correlation Analysis": correlation_analysis,
    "Distribution Analysis": distribution_analysis,
    "Demographic Distributions": demographic_distributions,
    "Travel Mode Analysis": travel_mode_analysis,
    "Vehicle Use Patterns": vehicle_use_patterns,
    "Activity Analysis": activity_analysis
}

if __name__ == "__main__":
    app()
