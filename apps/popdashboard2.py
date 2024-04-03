import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import os


#We will add a chloropleth
def load_geodata(filename):
    # Here we use the "newlyexportedshp" directory as part of the path
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)  # Move up one directory from the current file's location
    geojson_path = os.path.join(project_root, "newlyexportedshp", filename)

    if os.path.exists(geojson_path):
        return gpd.read_file(geojson_path)
    else:
        st.error(f"GeoJSON file not found at {geojson_path}")
        return gpd.GeoDataFrame()
def create_choropleth(geodata, population_data):
    # Merge the geodata with population data on the 'id' column
    merged_data = geodata.merge(population_data, how='left', left_on='id', right_on='id')
    
    # Ensure the correct column is used for the color scale. It might be '_sum_x' or '_sum_y' after the merge.
    # You should choose the correct one based on which DataFrame contains the population data you want to display.
    # For this example, we assume '_sum_x' is the correct column.
    population_column = 'M_30sum_x' if 'M_30sum_x' in merged_data else '_sum_y'
    
    # Create choropleth map using Plotly
    # Create choropleth map using Plotly
    fig = px.choropleth(merged_data,
                        geojson=merged_data.geometry,
                        locations=merged_data.index,
                        color=population_column,
                        color_continuous_scale="Blues",  # Blue color scale
                        title="Population by Area")
    
    # Set the layout for a dark background
    fig.update_layout(
        title_text="Total Population",
        title_x=0.5,
        geo=dict(
            landcolor='rgb(217, 217, 217)',  # Light grey color for the map
            lakecolor='rgb(255, 255, 255)',  # White color for lakes
            bgcolor='rgb(10, 10, 10)',  # Dark background for the outside map area
            showocean=True, oceancolor='rgb(10, 10, 10)',  # Dark color for the ocean
            subunitcolor='rgb(255, 255, 255)'  # White borders for states
        ),
        paper_bgcolor='rgb(10, 10, 10)',  # Dark background for the plot area
        margin={"r":0, "t":0, "l":0, "b":0},
        coloraxis_colorbar=dict(
            title="Population",
            thicknessmode="pixels", thickness=15,
            lenmode="pixels", len=300,
            yanchor="top", y=0.99,
            ticks="outside", ticksuffix=" people"
        )
    )
    
    # Remove axis lines and grid lines
    fig.update_geos(
        showcountries=True, countrycolor="White",
        showsubunits=True, subunitcolor="White",
        showland=True, landcolor="rgb(217, 217, 217)",
        showlakes=True, lakecolor="rgb(255, 255, 255)",
        showocean=True, oceancolor="rgb(10, 10, 10)",
        fitbounds="locations",
        visible=False
    )

    return fig



#-----We will agregate the age groups-----
def load_data(filename):
    # Dynamically construct the path to the data file
    base_path = os.path.dirname(__file__)
    project_root = os.path.join(base_path, os.pardir)
    data_path = os.path.join(project_root, "newlyexportedshp", filename)

    # Ensure the data file path exists
    if os.path.exists(data_path):
        # Read the CSV data file
        return pd.read_csv(data_path)
    else:
        st.error(f"Data file not found at {data_path}")
        return pd.DataFrame()

def aggregate_age_groups(data):
            # Define age groups
            age_groups = {
                '0-15': ['0', '1', '5', '10', '15'],
                '16-30': ['20', '25', '30'],
                '31-45': ['35', '40', '45'],
                '46-60': ['50', '55', '60'],
                '61-80': ['65', '70', '75', '80']
            }

            # Create a new DataFrame to store aggregated data
            aggregated_data = pd.DataFrame()

            for gender in ['M', 'F']:
                for group, ages in age_groups.items():
                    # Sum populations for each age group and gender
                    column_names = [f"{gender}_{age}sum" for age in ages]
                    aggregated_data[f'{gender}_{group}'] = data[column_names].sum(axis=1)

            aggregated_data['id'] = data['id']  # Ensure we keep the neighborhood identifier
            return aggregated_data


def app():
    st.title("Population Dashboard")

    # Load the dataset
    data = load_data('HexagonDemographicStatistics_AllBands_CSV.csv')

    #-----Lets visualise our chloropleth first-----
    # Load GeoJSON and population data
    geodata = load_geodata('HexagonDemographicStatistics_AllBands1.geojson')
    population_data = load_data('HexagonDemographicStatistics_AllBands_CSV.csv')

    # Check if the GeoJSON and population data have been loaded successfully
    if not geodata.empty and not population_data.empty:
        # Create and display the choropleth map
        choropleth_fig = create_choropleth(geodata, population_data)
        st.plotly_chart(choropleth_fig, use_container_width=True)

    #-----We can continue with other visualisation fucntions----
    if not data.empty:
        # Apply a threshold to filter out neighborhoods with insignificant populations for clarity in visualization
        threshold = st.slider('Population Sum Threshold for Visualization', min_value=10, max_value=2000, value=10, step=10)
        significant_data = data[data['_sum'] > threshold]

        # Display Overall Population Distribution Across All Significant Neighborhoods
        st.header('Overall Population Distribution Across Neighborhoods')
        fig_overall = px.bar(significant_data, x='id', y='_sum', labels={'_sum': 'Population Sum'}, title="Population Sum by Neighborhood")
        st.plotly_chart(fig_overall)

        # Interactive Gender and Age Cohort Distribution Visualizations
        st.header('Detailed Gender and Age Cohort Distribution')

        # Option to select specific gender for detailed visualization
        gender_option = st.selectbox('Select Gender for Visualization', ['F', 'M'])

        gender_data = significant_data[[col for col in significant_data.columns if col.startswith(gender_option)] + ['id']]
        # Melt the dataframe for better visualization handling
        gender_data = gender_data.melt(id_vars=['id'], var_name='Age Cohort', value_name='Population')
        # Improve readability of age cohorts in the visualization
        gender_data['Age Cohort'] = gender_data['Age Cohort'].apply(lambda x: x.replace(gender_option + '_', '') + ' years (' + gender_option + ')')
        # Generate and display the Plotly bar chart for selected gender
        fig_gender_age = px.bar(gender_data, x='id', y='Population', color='Age Cohort', title=f"Population by Age Cohort for {gender_option} across Neighborhoods")
        st.plotly_chart(fig_gender_age)

        # Additional Chart: Age Cohort Comparison within and across Neighborhoods
        st.header('Age Cohort Comparison within and across Neighborhoods')
        cohort_columns = [col for col in data.columns if col.endswith('sum') and col != '_sum']
        cohort_data = significant_data[cohort_columns + ['id']]
        cohort_data = cohort_data.melt(id_vars=['id'], var_name='Age Cohort', value_name='Population')
        cohort_data['Age Cohort'] = cohort_data['Age Cohort'].apply(lambda x: x.split('_')[1] + ' years (' + x.split('_')[0] + ')')
        fig_cohorts_comparison = px.bar(cohort_data, x='id', y='Population', color='Age Cohort', barmode='group', title="Age Cohort Comparison across Neighborhoods")
        st.plotly_chart(fig_cohorts_comparison)
        # Additional visualizations for deeper insights into the data can be added here
        # Examples: Age cohort comparison within each gender, neighborhood comparisons, etc.

                    # Call the aggregation function on your significant_data DataFrame
        aggregated_data = aggregate_age_groups(significant_data)

            # Generate a visualization for the aggregated age groups
        st.header('Broad Age Group Comparison across Neighborhoods')

            # Melt the aggregated data for visualization
        melted_aggregated_data = aggregated_data.melt(id_vars=['id'], var_name='Group', value_name='Population')

            # Create and display the Plotly chart
        fig_age_groups = px.bar(melted_aggregated_data, x='id', y='Population', color='Group', barmode='group', title="Population by Broad Age Groups across Neighborhoods")
        st.plotly_chart(fig_age_groups)

        



if __name__ == "__main__":
    app()
