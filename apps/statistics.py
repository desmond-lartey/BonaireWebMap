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
        return pd.read_excel(data_path)
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()

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
                sns.histplot(data[col], kde=True, ax=axes[i] if len(num_cols) > 1 else axes)
                axes[i if len(num_cols) > 1 else None].set_title(f'Distribution of {col}')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.write("No numerical columns available for distribution analysis.")

    else:
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14, 18))
            color_palette = ["Set2", "Set3", "Pastel1", "Pastel2"]
            if question == "Demographic Distributions":
                demographics(data, axes, color_palette)
            elif question == "Travel Mode Analysis":
                travel_modes(data, axes, color_palette)
            plt.tight_layout()
            st.pyplot(fig)
        except ValueError as e:
            st.error(f"Error plotting graphs: {e}")

def demographics(data, axes, color_palette):
    sns.countplot(data=data, x='Gender', ax=axes[0, 0], palette=color_palette[0])
    axes[0, 0].set_title('Gender Distribution')
    sns.countplot(data=data, x='Agegroup', ax=axes[0, 1], palette=color_palette[1])
    axes[0, 1].set_title('Age Group Distribution')
    sns.countplot(data=data, x='Ethnicity', ax=axes[1, 0], palette=color_palette[2])
    axes[1, 0].set_title('Ethnicity Distribution')
    sns.countplot(data=data, x='Activitytype', ax=axes[1, 1], palette=color_palette[3])
    axes[1, 1].set_title('Activity Type Distribution')

def travel_modes(data, axes, color_palette):
    travel_mode_crosstab = pd.crosstab(data['Agegroup'], data['Travel'])
    sns.heatmap(travel_mode_crosstab, annot=True, fmt="d", cmap="viridis", ax=axes[0, 0])
    sns.countplot(data=data, x='Travel', ax=axes[0, 1], palette=color_palette[1])
    sns.countplot(data=data, x='Car', ax=axes[1, 0], palette=color_palette[2])


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

    if st.sidebar.button("Analyze"):
        plot_analysis(data, selected_question)

if __name__ == "__main__":
    app()
