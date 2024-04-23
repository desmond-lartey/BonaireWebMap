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


def plot_analysis(data, question, additional_data=None):
    if question == "Correlation Analysis":
        enhanced_correlation_analysis(data)
    elif question == "Cross Correlation Analysis":
        if additional_data is not None:
            cross_correlation_analysis(data, additional_data)
        else:
            st.error("Additional data needed for cross-correlation analysis is not provided.")
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
    else:
        st.error("Selected analysis type is not supported.")


def enhanced_correlation_analysis(data, title='Correlation Matrix'):
    numeric_data = data.select_dtypes(include=[np.number]).dropna()
    if numeric_data.empty or numeric_data.shape[1] < 2:
        st.write("Not enough numerical columns for correlation analysis.")
    else:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title(title)
        st.pyplot(fig)

def cross_correlation_analysis(data1, data2):
    # Ensure both data sets are numeric and have the same length
    numeric_data1 = data1.select_dtypes(include=[np.number]).dropna()
    numeric_data2 = data2.select_dtypes(include=[np.number]).dropna()

    # Check if both datasets have rows to concatenate correctly
    if len(numeric_data1) != len(numeric_data2):
        st.error("The datasets cannot be directly correlated due to differing number of rows.")
        return

    # Concatenate along the columns after ensuring the same number of rows
    combined_data = pd.concat([numeric_data1.reset_index(drop=True), numeric_data2.reset_index(drop=True)], axis=1)

    # Check if there are enough columns to compute a correlation matrix
    if combined_data.empty or combined_data.shape[1] < 2:
        st.write("Not enough numerical columns for cross-dataset correlation analysis.")
    else:
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(combined_data.corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Cross-Dataset Correlation Matrix')
        st.pyplot(fig)


def distribution_analysis(data):
    num_cols = data.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        n_cols = min(len(num_cols), 4)  # Display up to 4 histograms per row
        n_rows = (len(num_cols) + 3) // 4  # Calculate rows needed
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
        axes = axes.flatten()
        for i, col in enumerate(num_cols):
            sns.histplot(data[col], kde=True, ax=axes[i])
            axes[i].set_title(f'Distribution of {col}')
        plt.tight_layout()
        st.pyplot(fig)
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
    st.pyplot(fig)

def travel_mode_analysis(data):
    fig, axes = plt.subplots(2, 2, figsize=(14, 18))
    travel_mode_crosstab = pd.crosstab(data['Agegroup'], data['Travel'])
    sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="viridis", ax=axes[0, 0])
    axes[0, 0].set_title('Travel Mode by Age Group')
    sns.countplot(data=data, x='Travel', ax=axes[0, 1])
    axes[0, 1].set_title('Travel Mode Preferences')
    axes[0, 1].tick_params(axis='x', rotation=45)
    sns.countplot(data=data, x='Car', ax=axes[1, 0])
    axes[1, 0].set_title('Car Usage Frequency')
    axes[1, 0].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def vehicle_use_patterns(data):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    sns.countplot(data=data, x='Car', ax=axes[0], palette="Set3")
    axes[0].set_title('Car Usage Frequency')
    axes[0].tick_params(axis='x', rotation=45)
    sns.countplot(data=data, x='Bicycle', ax=axes[1], palette="Set2")
    axes[1].set_title('Bicycle Usage Frequency')
    axes[1].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def activity_analysis(data):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    sns.countplot(data=data, x='Activitytype', ax=axes[0], palette="Pastel1")
    axes[0].set_title('Activity Type Distribution')
    axes[0].tick_params(axis='x', rotation=45)
    sns.countplot(data=data, x='Timeofday', ax=axes[1], palette="Pastel2")
    axes[1].set_title('Time of Day Distribution')
    axes[1].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


def app():
    # Load and prepare data
    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')

    # Convert data as necessary
    observations_numeric_data, observations_categorical_data = convert_categorical_to_numeric(observations_data)

    # User interface for data selection
    st.sidebar.title("User Selection")
    dataset_choice = st.sidebar.radio("Choose the dataset:", ('Observations', 'Survey'))
    data = observations_numeric_data if dataset_choice == 'Observations' else survey_data

    # Display data option
    if st.sidebar.checkbox("Show Data"):
        st.write(data)

    # Define available questions
    questions = {
        'Observations': ["Demographic Distributions", "Activity Analysis", "Correlation Analysis", "Cross Correlation Analysis", "Distribution Analysis"],
        'Survey': ["Travel Mode Analysis", "Vehicle Use Patterns", "Correlation Analysis", "Cross Correlation Analysis", "Distribution Analysis"]
    }

    # Allow user to select a question
    selected_question = st.sidebar.selectbox("Select a question:", questions[dataset_choice])
    
    # Determine which analysis to perform based on the selection
    if "Cross Correlation Analysis" in selected_question:
        plot_analysis(observations_numeric_data, selected_question, data2=survey_data)
    else:
        plot_analysis(data, selected_question)




if __name__ == "__main__":
    app()
