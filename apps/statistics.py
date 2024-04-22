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
    else:
        fig, axes = plt.subplots(2, 2, figsize=(14, 18))
        if question == "Demographic Distributions":
            demographic_distributions(data, axes)
        elif question == "Travel Mode Analysis":
            travel_mode_analysis(data, axes)
        # plt.tight_layout()
        # st.pyplot(fig)


    plt.tight_layout()
    st.pyplot(fig)

def demographic_distributions(data, axes, color_palette):
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

def travel_mode_analysis(data, axes, color_palette):
    travel_mode_crosstab = pd.crosstab(data['Agegroup'], data['Travel'])
    sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="viridis", ax=axes[0, 0])
    axes[0, 0].set_title('Travel Mode by Age Group')
    sns.countplot(data=data, x='Travel', ax=axes[0, 1], palette=color_palette[1])
    axes[0, 1].set_title('Travel Mode Preferences')
    axes[0, 1].tick_params(axis='x', rotation=45)
    sns.countplot(data=data, x='Car', ax=axes[1, 0], palette=color_palette[2])
    axes[1, 0].set_title('Car Usage Frequency')
    axes[1, 0].tick_params(axis='x', rotation=45)

def correlation_analysis(data, axes):
    numerical_data = data.select_dtypes(include=[np.number])
    if numerical_data.shape[1] > 1:
        sns.heatmap(numerical_data.corr(), annot=True, cmap='coolwarm', ax=axes[0, 0])
        axes[0, 0].set_title('Correlation Matrix')
        # Hide other plots
        for i in range(1, 4):
            axes.flat[i].set_visible(False)
    else:
        st.write("Not enough numerical columns for correlation analysis.")

def distribution_analysis(data, fig):
    num_cols = data.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        n_rows = (len(num_cols) + 1) // 2  # Ensure there are enough rows to handle the columns
        fig, axes = plt.subplots(n_rows, 2, figsize=(14, 5 * n_rows))  # Adjust the figure size based on the number of rows
        axes = axes.flatten()  # Flatten the axes array to make indexing easier
        for i, col in enumerate(num_cols):
            sns.histplot(data[col], kde=True, ax=axes[i])
            axes[i].set_title(f'Distribution of {col}')
        for j in range(i + 1, len(axes)):  # Hide unused axes if any
            axes[j].set_visible(False)
        plt.tight_layout()
    else:
        st.write("No numerical columns available for distribution analysis.")


def app():
    st.title("Active Mobility Data Analysis")
    raw_observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')
    observations_numeric_data, observations_categorical_data = convert_categorical_to_numeric(raw_observations_data)

    st.sidebar.title("User Selection")
    dataset_choice = st.sidebar.radio("Choose the dataset:", ('Observations', 'Survey'))
    numeric_data = observations_numeric_data if dataset_choice == 'Observations' else survey_data
    categorical_data = observations_categorical_data if dataset_choice == 'Observations' else survey_data

    if st.sidebar.checkbox("Show Data"):
        st.write(categorical_data)  # Show categorical data for readability

    questions = {
        'Observations': ["Demographic Distributions", "Activity Analysis", "Correlation Analysis", "Distribution Analysis"],
        'Survey': ["Travel Mode Analysis", "Vehicle Use Patterns", "Correlation Analysis", "Distribution Analysis"]
    }

    selected_question = st.sidebar.selectbox("Select a question:", questions[dataset_choice])
    if "Correlation Analysis" in selected_question or "Distribution Analysis" in selected_question:
        plot_analysis(numeric_data, selected_question)
    else:
        plot_analysis(categorical_data, selected_question)  # Use categorical data for non-numerical analysis

if __name__ == "__main__":
    app()
