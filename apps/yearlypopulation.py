import streamlit as st
import plotly.express as px
import pandas as pd
import os

# Function to load the neighborhood population data, correctly navigating the directory structure
def load_neighborhood_population_data(filename="NeighborhoodPopulationByYear_CSV.csv"):
    # Adjusted logic to match your directory structure
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)  # Move up one directory from the current file's location
    csv_path = os.path.join(project_root, "newlyexportedshp", filename)
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        st.error(f"CSV file not found at {csv_path}")
        return pd.DataFrame()

# Adjusted Function to create a treemap for neighborhood population data
def create_neighborhood_treemap(data):
    # Melt the DataFrame to long format with 'Year' as the variable name and 'Population_Sum' as the value
    melted_data = data.melt(id_vars=["id"], value_vars=['2000', '2005', '2010', '2015', '2020'], 
                            var_name='Year', value_name='Population_Sum')
    
    # Creating the treemap
    fig = px.treemap(
        melted_data,
        path=['Year', 'id'],  # Use 'Year' and 'id' in the path for hierarchical grouping
        values='Population_Sum',
        color='Population_Sum',  # Color based on the Population_Sum to show size proportion
        color_continuous_scale='Viridis',
        title='Neighborhood Population by Year'
    )
    
    # Adjust layout for readability
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.update_traces(textinfo='label+value')  # Show 'id' and population sum on the treemap

    return fig

# Define the Streamlit app
def app():
    st.title("Population Data Visualization")

    # Sample population data with years and population sums
    population_data = pd.DataFrame({
        'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
        'year': [2000, 2005, 2010, 2015, 2020]
    })

    # Treemap and Scatter plot visualization code...

    # Load neighborhood population data and create the third treemap
    neighborhood_data = load_neighborhood_population_data("NeighborhoodPopulationByYear_CSV.csv")
    if not neighborhood_data.empty:
        # Assuming ".geo" column exists and can be used as a unique identifier
        neighborhood_treemap_fig = create_neighborhood_treemap(neighborhood_data)
        st.plotly_chart(neighborhood_treemap_fig, use_container_width=True)

# Run the Streamlit app
if __name__ == '__main__':
    app()
