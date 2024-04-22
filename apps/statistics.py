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
    plt.figure(figsize=(10, 6))
    
    if question == "Activity Type Distribution":
        # Distribution of activity types, useful for understanding the most common activities.
        sns.countplot(data=data, x='Activitytype')
        plt.title('Distribution of Activity Types')
        plt.xticks(rotation=45)

    elif question == "Gender Distribution":
        # Gender distribution across activities to see if there's a gender bias in activity participation.
        sns.countplot(data=data, x='Gender')
        plt.title('Gender Distribution')

    elif question == "Peak Activity Times":
        # Visualization of activity frequency by time of day to identify peak activity times.
        sns.countplot(data=data, x='Timeofday')
        plt.title('Peak Activity Times')
        plt.xticks(rotation=45)

    elif question == "Travel Mode Preferences":
        # Travel mode preferences by age group to target specific age demographics.
        travel_mode_age = pd.crosstab(data['Age'], data['Travel'])
        sns.heatmap(travel_mode_age, annot=True, fmt="d", cmap="Blues")
        plt.title('Travel Mode Preferences by Age Group')

    elif question == "Income Distribution":
        # Income distribution to assess economic factors influencing travel choices.
        data['Income'].plot(kind='hist', bins=10, color='skyblue')
        plt.title('Income Distribution')
        plt.xlabel('Income Levels')

    st.pyplot(plt)


def app():
    st.title("Active Mobility Data Analysis")

    # Load Data
    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')

    # Sidebar for user interaction
    st.sidebar.title("User Selection")
    dataset_choice = st.sidebar.radio("Choose the dataset:", ('Observations', 'Survey'))
    data = observations_data if dataset_choice == 'Observations' else survey_data

    # Define questions based on the selected dataset
    if dataset_choice == 'Observations':
        questions = ["Activity Type Distribution", "Gender Distribution"]  # Extend with more relevant questions
    elif dataset_choice == 'Survey':
        questions = ["Travel Mode Preferences", "Income Distribution"]  # Extend with more relevant questions

    # Select question for analysis
    selected_question = st.sidebar.selectbox("Select a question:", questions)

    # Button to perform analysis
    if st.sidebar.button("Analyze"):
        plot_analysis(data, selected_question)


if __name__ == "__main__":
    app()
