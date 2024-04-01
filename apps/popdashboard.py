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
# Load and prepare data
def load_data():
    # Adjust the path to directly point to your CSV file within the 'newlyexportedshp' folder
    file_path = os.path.join(os.path.dirname(__file__), "newlyexportedshp", "HexagonDemographicStatistics_AllBands_CSV.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Add any necessary data preprocessing steps here
        return df
    else:
        st.error(f"CSV file not found at {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found


# Ensure the file name matches your CSV file name without the extension
df = load_data()

# Additional code for visualization and dashboard setup here
# Example: Function to create bar chart visualization
def create_bar_chart(df, sex, age_group):
    column_name = f"{sex}_{age_group}_sum"
    bar_chart = px.bar(df, x='hex_id', y=column_name,
                       title=f"Population Sum for {age_group} Year Olds ({sex})",
                       labels={'hex_id': 'Hexagon ID', column_name: 'Population Sum'})
    return bar_chart

# Main app function
def app():
    apply_custom_css()
    st.title("Hexagon Population Dashboard")

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
