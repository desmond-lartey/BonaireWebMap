import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Initial population data
base_population_data = pd.DataFrame({
    'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
    'year': [2000, 2005, 2010, 2015, 2020]
})

# Function to simulate additional data points for the violin plot
def simulate_data(row):
    year_as_int = int(row['year'])  # Convert year to an integer for the random seed
    np.random.seed(year_as_int)  # Set the seed
    # Generate a normal distribution around the population_sum value
    return pd.Series(np.random.normal(loc=row['population_sum'], scale=row['population_sum'] / 10, size=100))

# Apply the simulate_data function to the population data
simulated_population = base_population_data.apply(simulate_data, axis=1).stack().reset_index(level=1, drop=True)
simulated_population.name = 'population_sum'  # Name the Series so it can be joined to the base data
# Join the simulated population data to the base data's year column
simulated_data = base_population_data.drop(columns='population_sum').join(simulated_population)

# Altair code for the violin plot
def create_violin_plot(data):
    chart = alt.Chart(data).transform_density(
        'population_sum',
        as_=['population_sum', 'density'],
        extent=[data.population_sum.min(), data.population_sum.max()],
        groupby=['year']
    ).mark_area(
        orient='vertical',
        opacity=0.6
    ).encode(
        alt.X('year:O', title='Year'),
        alt.Y('density:Q'),
        color='year:N',
    ).properties(
        width=100,
        height=300
    ).configure_facet(
        spacing=10
    ).configure_view(
        strokeWidth=0
    )
    
    return chart

# Streamlit app code
def app():
    st.title('Population Data Visualization')
    # Create the violin plot
    violin_plot = create_violin_plot(simulated_data)
    # Display the plot
    st.altair_chart(violin_plot, use_container_width=True)

# Run the app
if __name__ == '__main__':
    app()
