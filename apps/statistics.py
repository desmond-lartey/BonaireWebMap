import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

def load_data(filename):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    data_path = os.path.join(project_root, filename)
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
    # Check if data has numerical columns for these analyses
    numerical_data = data.select_dtypes(include=[np.number])
    if numerical_data.empty:
        st.write("No numerical columns available for this analysis.")
        return

    if "Correlation Analysis" in question:
        plt.figure(figsize=(10, 8))
        sns.heatmap(numerical_data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        st.pyplot(plt)

    elif "Distribution Analysis" in question:
        num_cols = numerical_data.columns
        fig, axes = plt.subplots(1, len(num_cols), figsize=(5 * len(num_cols), 4))
        for i, col in enumerate(num_cols):
            sns.histplot(numerical_data[col], kde=True, ax=axes[i] if len(num_cols) > 1 else axes)
            axes[i if len(num_cols) > 1 else None].set_title(f'Distribution of {col}')
        plt.tight_layout()
        st.pyplot(fig)

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
    # Automatically plot analysis when a question is selected
    plot_analysis(data, selected_question)  

if __name__ == "__main__":
    app()
