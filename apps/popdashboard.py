import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Inline CSS
CUSTOM_CSS = """
<style>
/* Custom styles */
[data-testid="stSidebar"] { background-color: #f0f2f6; }
[data-testid="stHeader"] { background-color: #ffffff; }
/* Add more custom styles as needed */
</style>
"""

# Apply custom CSS
def apply_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Load and prepare data
def load_data(file_name):
    # Dynamic file path construction
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    file_path = os.path.join(project_root, "newlyexportedshp", "HexagonDemographicStatistics_AllBands_CSV")  # Adjust folder name as needed
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Preprocess data here if needed
        return df
    else:
        st.error(f"CSV file not found at {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if file is not found

# Create bar chart visualization
def create_bar_chart(df, sex, age_group):
    column_name = f"{sex}_{age_group}_sum"  # Use '_sum' to aggregate population
    bar_chart = px.bar(df, x='hex_id', y=column_name,
                       title=f"Population Sum for {age_group} Year Olds ({sex})",
                       labels={'hex_id': 'Hexagon ID', column_name: 'Population Sum'})
    return bar_chart

# Main app function
def app():
    apply_custom_css()
    st.title("Hexagon Population Dashboard")

    # Load data
    df = load_data("HexagonDemographicStatistics_AllBands_CSV.csv")
    if df.empty:
        return  # Early exit if no data

    # Sidebar for filter selection
    age_groups = sorted(set(col.split("_")[1] for col in df.columns if col.startswith(("F_", "M_"))))
    selected_age_group = st.sidebar.selectbox("Select an Age Group", age_groups)
    sex_options = ['F', 'M']
    selected_sex = st.sidebar.selectbox("Select Sex", sex_options)

    # Display the bar chart based on user selection
    st.plotly_chart(create_bar_chart(df, selected_sex, selected_age_group), use_container_width=True)

    # Additional data presentation
    st.header("Top Hexagons")
    top_hexagons = df.nlargest(5, f'{selected_sex}_{selected_age_group}_sum')
    st.write(top_hexagons[['hex_id', f'{selected_sex}_{selected_age_group}_sum']])

    # Footer with additional info
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This dashboard visualizes population demographics across different hexagons.")

if __name__ == "__main__":
    app()
