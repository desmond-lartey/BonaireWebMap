#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import plotly.graph_objects as go


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
        enhanced_correlation_analysis(data)
    elif question == "Distribution Analysis":
        distribution_analysis(data)
    elif question == "Demographic Distributions":
        demographic_distributions(data)
    elif question == "Travel Mode Analysis":
        travel_mode_analysis(data)
    elif question == "Vehicle Use Patterns":
        vehicle_use_patterns(data)
    elif question == "Activity Analysis":
        activity_analysis(data)
    elif question == "Cross Correlation Analysis":
        # Ensure that the correct numeric datasets are loaded for cross-correlation
        observations_numeric_data = load_data('Bonaire_Observations3.xlsx')
        survey_numeric_data = load_data('Bonaire_Survey3.xlsx')
        combined_data = merge_datasets(observations_numeric_data, survey_numeric_data)
        cross_correlation_analysis(combined_data)
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

def merge_datasets(data1, data2):
    # Define common columns used for merging
    common_columns = ['Gender', 'Agegroup']

    # Merge the datasets on these common columns
    combined_data = pd.merge(data1, data2, on=common_columns, how='inner')

    
    # This approach assumes all columns needed for analysis are kept
    combined_data = combined_data[[col for col in data1.columns if col in common_columns] + 
                                  ['Ethnicity', 'Site', 'Activitytype', 'Timeofday', 'Travel', 'Car', 'Income', 'Bicycle', 'Country', 'Household']]

    # Debugging: Print or log the structure of the merged data to verify it contains what you expect
    st.write("Combined Data Structure:", combined_data.head())
    st.write("Numeric columns available for analysis:", combined_data.select_dtypes(include=[np.number]).columns)

    return combined_data





def cross_correlation_analysis(combined_data):
    numeric_data = combined_data.select_dtypes(include=[np.number])
    if numeric_data.empty or numeric_data.shape[1] < 2:
        st.write("Not enough numerical columns for cross-dataset correlation analysis.")
    else:
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', ax=ax)
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

def create_sankey_data(data, source_col, target_col):
    # Count the frequency of source-target pairs
    counts = data.groupby([source_col, target_col]).size().reset_index(name='Counts')
    
    # Create mappings for source and target
    source_mapping = {source: idx for idx, source in enumerate(counts[source_col].unique())}
    target_mapping = {target: idx+len(source_mapping) for idx, target in enumerate(counts[target_col].unique())}
    
    # Apply mappings to get source and target indices
    counts['source_idx'] = counts[source_col].map(source_mapping)
    counts['target_idx'] = counts[target_col].map(target_mapping)
    
    return counts, list(source_mapping.keys()) + list(target_mapping.keys())

# Function to plot the Sankey diagram
def plot_sankey_chart(data, source_col='Site', target_col='Activitytype'):
    counts, labels = create_sankey_data(data, source_col, target_col)
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=counts['source_idx'],
            target=counts['target_idx'],
            value=counts['Counts']
        ))])
    
    fig.update_layout(title_text=f"{target_col} by {source_col} Relationship", font_size=10)
    st.plotly_chart(fig, use_container_width=True)


def app():
    st.title("Active Mobility Data Analysis")

    # Load and prepare data
    observations_data = load_data('Bonaire_Observations2.xlsx')
    survey_data = load_data('Bonaire_Survey2.xlsx')
    observations_numeric_data = load_data('Bonaire_Observations3.xlsx')
    survey_numeric_data = load_data('Bonaire_Survey3.xlsx')

    st.sidebar.title("User Selection")
    dataset_choice = st.sidebar.radio("Choose the dataset for analysis:", ('Observations', 'Survey'))
    analysis_type = st.sidebar.radio("Choose the type of analysis:", ['Single Dataset Analysis', 'Cross-Dataset Analysis', 'Predictive Analysis'])

    # Single Dataset Analysis
    if analysis_type == 'Single Dataset Analysis':
        data = observations_data if dataset_choice == 'Observations' else survey_data
        if st.sidebar.checkbox("Show Data"):
            st.write(data)  # Show the readable version of the data

        questions = {
            'Observations': ["Demographic Distributions", "Activity Analysis", "Correlation Analysis", "Distribution Analysis", "Site Related Analysis"],
            'Survey': ["Travel Mode Analysis", "Vehicle Use Patterns", "Correlation Analysis", "Distribution Analysis"]
        }

        selected_question = st.sidebar.selectbox("Select a question:", questions[dataset_choice])
        if selected_question == "Site Related Analysis":
            plot_sankey_chart(observations_data)  # Call the function to plot the Sankey chart
        elif selected_question in ["Correlation Analysis", "Distribution Analysis"]:
            plot_analysis(observations_numeric_data if dataset_choice == 'Observations' else survey_numeric_data, selected_question)
        else:
            plot_analysis(data, selected_question)

    # Cross-Dataset Analysis
    elif analysis_type == 'Cross-Dataset Analysis':
        if st.sidebar.button("Perform Cross Correlation Analysis"):
            combined_data = merge_datasets(observations_numeric_data, survey_numeric_data)  # Prepare combined data for cross-correlation
            cross_correlation_analysis(combined_data)  # Perform cross-dataset correlation analysis

    # Predictive Analysis
    elif analysis_type == "Predictive Analysis":
        st.subheader("Predictive Model Results")
        if st.sidebar.button("Run Prediction Model"):
            # Placeholder for predictive analysis
            st.write("Predictive Model would be implemented here")
            # Placeholder for predicted plots
            st.write("Current (2024) Predictions:")
            st.pyplot()  # Replace with actual plot
            st.write("Predictions for 2028:")
            st.pyplot()  # Replace with actual plot
            st.write("Predictions for 2038:")
            st.pyplot()  # Replace with actual plot

# Call the app function to run the app
if __name__ == "__main__":
    app()

