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
    if question == "Correlation Analysis":
        correlation_analysis(data)
    elif question == "Distribution Analysis":
        distribution_analysis(data)
    elif question == "Demographic Distributions":
        demographic_distributions(data)
    elif question == "Travel Mode Analysis":
        travel_mode_analysis(data)
    elif question == "Vehicle Use Patterns":
        vehicle_use_patterns(data)  # For survey
    elif question == "Activity Analysis":
        activity_analysis(data)  # For observations


def correlation_analysis(data):
    if data.select_dtypes(include=[np.number]).shape[1] > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        st.pyplot()
    else:
        st.write("Not enough numerical columns for correlation analysis.")

def distribution_analysis(data):
    num_cols = data.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        fig, axes = plt.subplots(1, len(num_cols), figsize=(5 * len(num_cols), 4))
        for i, col in enumerate(num_cols):
            sns.histplot(data[col], kde=True, ax=axes[i])
            axes[i].set_title(f'Distribution of {col}')
        plt.tight_layout()
        st.pyplot()
    else:
        st.write("No numerical columns available for distribution analysis.")

def demographic_distributions(data):
    fig, axes = plt.subplots(2, 2, figsize=(14, 18))
    color_palette = ["Set2", "Set3", "Pastel1", "Pastel2"]
    sns.countplot(data=data, x='Gender', ax=axes[0, 0], palette=color_palette[0])
    axes[0, 0].set_title('Gender Distribution')
    sns.countplot(data=data, x='Agegroup', ax=axes[0, 1], palette=color_palette[1])
    axes[0, 1].set_title('Age Group Distribution')
    sns.countplot(data=data, x='Ethnicity', ax=axes[1, 0], palette=color_palette[2])
    axes[1, 0].set_title('Ethnicity Distribution')
    sns.countplot(data=data, x='Activitytype', ax=axes[1, 1], palette=color_palette[3])
    axes[1, 1].set_title('Activity Type Distribution')
    plt.tight_layout()
    st.pyplot()

def travel_mode_analysis(data):
    fig, axes = plt.subplots(2, 2, figsize=(14, 18))
    travel_mode_crosstab = pd.crosstab(data['Agegroup'], data['Travel'])
    sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="viridis", ax=axes[0, 0])
    axes[0, 0].set_title('Travel Mode by Age Group')
    sns.countplot(data=data, x='Travel', ax=axes[0, 1])
    axes[0, 1].set_title('Travel Mode Preferences')
    sns.countplot(data=data, x='Car', ax=axes[1, 0])
    axes[1, 0].set_title('Car Usage Frequency')
    plt.tight_layout()
    st.pyplot()

def vehicle_use_patterns(data):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    sns.countplot(data=data, x='Car', ax=axes[0], palette="Set3")
    axes[0].set_title('Car Usage Frequency')
    axes[0].tick_params(axis='x', rotation=45)
    
    sns.countplot(data=data, x='Bicycle', ax=axes[1], palette="Set2")
    axes[1].set_title('Bicycle Usage Frequency')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot()

def activity_analysis(data):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    sns.countplot(data=data, x='Activitytype', ax=axes[0], palette="Pastel1")
    axes[0].set_title('Activity Type Distribution')
    axes[0].tick_params(axis='x', rotation=45)
    
    # If you have another relevant categorical variable to show, replace 'ExampleCategory' with that variable name.
    # For example, if you want to show data based on time of day or another aspect:
    sns.countplot(data=data, x='Timeofday', ax=axes[1], palette="Pastel2")
    axes[1].set_title('Time of Day Distribution')
    axes[1].tick_params(axis='x', rotation=45)
    
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
    plot_analysis(data, selected_question)  # Automatically plot when a question is selected

if __name__ == "__main__":
    app()
