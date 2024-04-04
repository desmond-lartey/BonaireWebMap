import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

# Base population data
base_population_data = pd.DataFrame({
    'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
    'year': [2000, 2005, 2010, 2015, 2020]
})

# Simulate multiple observations around the given population numbers
# Create a wider distribution for larger populations and a narrower one for smaller populations
def simulate_data(row):
    np.random.seed(row['year'])  # Ensure reproducibility
    return np.random.normal(loc=row['population_sum'], scale=row['population_sum'] / 10, size=100)

# Apply the simulation to each row
simulated_data = base_population_data.apply(simulate_data, axis=1).explode().reset_index(drop=True)
simulated_data = pd.DataFrame({
    'population_sum': simulated_data,
    'year': np.repeat(base_population_data['year'], 100)
})

# Convert population_sum to numeric
simulated_data['population_sum'] = pd.to_numeric(simulated_data['population_sum'])

# Function to create a violin plot
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
        alt.X('year:O', title='Year'),  # Treat 'year' as an ordinal variable for discrete x-axis
        alt.Y('density:Q'),
        color='year:N',
        row=alt.Row('year:N', header=alt.Header(title='Year', labelAngle=0))  # Use row instead of column for horizontal layout
    ).properties(
        width=100,
        height=400
    ).configure_facet(
        spacing=10  # Add some spacing between rows
    ).configure_view(
        stroke=None
    )
    
    return chart

def app():
    st.title('Population Data Visualization')

    # Create and display the violin plot
    violin_plot = create_violin_plot(simulated_data)
    st.altair_chart(violin_plot, use_container_width=True)

if __name__ == '__main__':
    app()
