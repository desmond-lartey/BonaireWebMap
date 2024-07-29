import streamlit as st
import plotly.express as px
import pandas as pd
import os
import numpy as np

# Correctly navigating the directory structure to load neighborhood population data
def load_neighborhood_population_data(filename="NeighborhoodPopulationByYear_CSV.csv"):
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)  # Move up one directory from the current file's location
    csv_path = os.path.join(project_root, "newlyexportedshp", filename)
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        st.error(f"CSV file not found at {csv_path}")
        return pd.DataFrame()

# Adjusted function to create a treemap for neighborhood population data considering the new data structure
@st.experimental_memo
def create_neighborhood_treemap(data):
    # Ensure column names exist in DataFrame before melting
    existing_columns = data.columns.tolist()
    years = ['2000', '2005', '2010', '2015', '2020', '2024', '2028', '2038']
    value_vars = [year for year in years if year in existing_columns]
    
    if not value_vars:
        st.error("None of the specified years are present in the data.")
        return None

    melted_data = data.melt(id_vars=["id"], value_vars=value_vars, 
                            var_name='Year', value_name='Population_Sum')

    # Calculate a midpoint for coloring. Here, we'll use the average population as an approximation.
    color_midpoint = np.average(melted_data['Population_Sum'], weights=melted_data['Population_Sum'])

    fig = px.treemap(
        melted_data,
        path=[px.Constant("All Neighborhoods"), 'Year', 'id'],
        values='Population_Sum',
        color='Population_Sum',
        color_continuous_scale='RdBu',
        color_continuous_midpoint=color_midpoint
    )
    
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title_text='Neighborhood Population by Year')

    return fig

# Streamlit app definition
def app():
    st.title("Population")

    # Initial population data and treemap visualization
    population_data = pd.DataFrame({
        'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252, 25100, 29485, 44099],
        'year': [2000, 2005, 2010, 2015, 2020, 2024, 2028, 2038]
    })

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
        title="Population increase over Years"
    )
    scatter_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(scatter_fig, theme="streamlit")
    with tab2:
        st.plotly_chart(scatter_fig, theme=None)
    
    # Load neighborhood population data and add the third treemap
    neighborhood_data = load_neighborhood_population_data()
    if not neighborhood_data.empty:
        neighborhood_treemap_fig = create_neighborhood_treemap(neighborhood_data)
        st.plotly_chart(neighborhood_treemap_fig, use_container_width=True)

# Customize the sidebar
# st.sidebar.title("About")
# st.sidebar.info("A Streamlit map template\n<https://github.com/opengeos/streamlit-map-template>")

# Adding the logo image
logo_url = "https://urbancyclinginstitute.org/wp-content/uploads/2024/01/active-mobility-Bonaire.jpeg"
st.sidebar.image(logo_url, caption="Bonaire")


# Execute the Streamlit app
if __name__ == '__main__':
    app()


hide_github_icon = """
    <style>
        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, 
        .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, 
        .viewerBadge_text__1JaDK { display: none; } 
        #MainMenu { visibility: hidden; } 
        footer { visibility: hidden; } 
        header { visibility: hidden; }
    </style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)
