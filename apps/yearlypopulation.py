import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Sample data with multiple observations per year
data = pd.DataFrame({
    'population_sum': np.concatenate([
        np.random.normal(9531, 500, 100),   # Simulated population data for 2000
        np.random.normal(11662, 600, 100),  # Simulated population data for 2005
        np.random.normal(14270, 700, 100),  # Simulated population data for 2010
        np.random.normal(17462, 800, 100),  # Simulated population data for 2015
        np.random.normal(21367, 900, 100),  # Simulated population data for 2020
    ]),
    'year': ['2000'] * 100 + ['2005'] * 100 + ['2010'] * 100 + ['2015'] * 100 + ['2020'] * 100
})

# Function to create a violin plot
def create_violin_plot(df):
    violin_plot = alt.Chart(df).mark_area().encode(
        x=alt.X('year:N', axis=alt.Axis(labels=True, title='Year')),
        y=alt.Y('population_sum:Q', axis=alt.Axis(labels=True, title='Population')),
        color=alt.Color('year:N', scale=alt.Scale(scheme='category20b'))
    ).properties(
        width=100
    ).transform_density(
        density='population_sum',
        bandwidth=0.3,
        groupby=['year'],
        as_=['population_sum', 'density']
    )
    return violin_plot

# Creating the app
def app():
    st.title("Population Data Visualization")
    violin_chart = create_violin_plot(data)
    st.altair_chart(violin_chart, use_container_width=True)

if __name__ == "__main__":
    app()
