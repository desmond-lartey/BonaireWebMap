import altair as alt
import pandas as pd
import streamlit as st

# Sample population data from 2000 to 2020
population_data = pd.DataFrame({
    'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
    'year': [2000, 2005, 2010, 2015, 2020]
})

# Function to create a violin plot
def create_violin_plot(data):
    # Transform the data to create a density estimate for the violin plot
    violin_data = alt.Chart(data).transform_density(
        density='population_sum',  # Calculate density over the population
        groupby=['year'],  # Group by year for individual violins
        as_=['population_sum', 'density']
    ).mark_area(
        orient='vertical',  # Make the violins vertical
        opacity=0.6  # Set the opacity for the violins
    ).encode(
        alt.X('year:O', title='Year'),  # Year on the X-axis as ordinal
        alt.Y('population_sum:Q', title='Population', axis=alt.Axis(title='Population Sum')),  # Population on the Y-axis
        color=alt.Color('year:N', legend=alt.Legend(title="Origin"))  # Color by year with legend titled "Origin"
    ).properties(
        width=150,  # Width of each violin plot
        height=300  # Height of the violin plots
    )

    return violin_data

def app():
    st.title("Population Data Visualization")

    # Create and display the violin plot
    violin_plot = create_violin_plot(population_data)
    st.altair_chart(violin_plot, use_container_width=True)

# Run the app function if the script is executed
if __name__ == '__main__':
    app()
