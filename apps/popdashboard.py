import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Apply the custom CSS from the template you provided
def apply_custom_css():
    with open(os.path.join(os.path.dirname(__file__), "style.css")) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data function adapted to fit the dynamic file path logic
def load_data(file_name):
    base_path = os.path.dirname(__file__)  # Gets the directory where the script is located
    file_path = os.path.join(base_path, "data", file_name)  # Adjust folder and file names as needed
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"CSV file not found at {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found

# Function to create bar chart visualizations
def create_bar_chart(df, sex, age_group):
    df_filtered = df[df["sex"] == sex]
    bar_chart = px.bar(df_filtered, x='hex_id', y=f'{sex}_{age_group}', 
                       title=f"Population for {age_group} Year Olds ({sex})",
                       labels={'hex_id': 'Hexagon ID', f'{sex}_{age_group}': 'Population'})
    return bar_chart

# Main app function for the population dashboard
def app():
    apply_custom_css()
    st.title("Hexagon Population Dashboard")

    # Sidebar filters for age group and sex
    df = load_data("HexagonDemographicStatistics_AllBands_CSV.csv")
    if df.empty:
        st.error("No data to display.")
        return

    age_groups = [col.split("_")[1] for col in df.columns if "_" in col and col.endswith("mean")]
    selected_age_group = st.sidebar.selectbox("Select an Age Group", sorted(set(age_groups)))
    sex_options = ['Female', 'Male']
    selected_sex = st.sidebar.radio("Select Sex", sex_options)

    # Main panel
    col1, col2 = st.columns([3, 1])
    with col1:
        # Main visualization (bar chart)
        st.plotly_chart(create_bar_chart(df, selected_sex, selected_age_group), use_container_width=True)

    with col2:
        # Top statistics or additional data presentation
        # For example, displaying top hexagons by population
        st.header("Top Hexagons")
        top_hexagons = df.nlargest(5, f'{selected_sex}_{selected_age_group}')
        st.write(top_hexagons[['hex_id', f'{selected_sex}_{selected_age_group}']])

    # Footer
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This dashboard is powered by data from the HexagonDemographicStatistics project.")

# Ensure to call this function in your main.py or add it to the app's navigation
