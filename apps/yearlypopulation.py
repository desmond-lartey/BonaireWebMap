import streamlit as st
import plotly.express as px
import pandas as pd
import os

# Function to load the neighborhood population data
def load_neighborhood_population_data(filename="NeighborhoodPopulationByYear_CSV.csv"):
    # Construct the path to the CSV file within the 'newlyexportedshp' directory
    file_path = os.path.join(os.path.dirname(__file__), "newlyexportedshp", filename)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"CSV file not found at {file_path}")
        return pd.DataFrame()

# Function to create a treemap for neighborhood population data
def create_neighborhood_treemap(data):
    fig = px.treemap(data, 
                     path=['year', 'id'],  # Assuming 'id' is a unique identifier for each neighborhood
                     values='_sum',  # Population sum for each neighborhood
                     color='_sum',  # Color the blocks by population sum
                     color_continuous_scale='Viridis'  # Using a different color scale for distinction
                    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title_text='Neighborhood Population by Year')
    return fig

# Define the Streamlit app
def app():
    st.title("Population Data Visualization")

    # Sample population data with years and population sums
    population_data = pd.DataFrame({
        'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
        'year': [2000, 2005, 2010, 2015, 2020]
    })

    # Treemap visualization for general population data
    population_data['year_str'] = population_data['year'].astype(str)
    treemap_fig = px.treemap(
        population_data,
        path=['year_str'],
        values='population_sum',
        color='population_sum',
        color_continuous_scale='Blues'
    )
    treemap_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title_text='Population by Year')
    st.plotly_chart(treemap_fig, use_container_width=True)

    # Scatter plot visualization
    scatter_fig = px.scatter(
        population_data,
        x="year",
        y="population_sum",
        size="population_sum",
        hover_name="year",
        size_max=60,
        title="Population Scatter Plot over Years"
    )
    scatter_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(scatter_fig, theme="streamlit")
    with tab2:
        st.plotly_chart(scatter_fig, theme=None)
    
    # Load neighborhood population data and create the third treemap
    neighborhood_data = load_neighborhood_population_data()
    if not neighborhood_data.empty:
        neighborhood_treemap_fig = create_neighborhood_treemap(neighborhood_data)
        st.plotly_chart(neighborhood_treemap_fig, use_container_width=True)

# Run the Streamlit app
if __name__ == '__main__':
    app()
