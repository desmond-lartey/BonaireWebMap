import altair as alt
import pandas as pd
import streamlit as st

# Dummy data representing multiple observations per year
# Replace this with your actual DataFrame with multiple observations per year
population_data = pd.DataFrame({
    'population_sum': [
        9531.1, 9600.2, 9800.1,  # Multiple data points for the year 2000
        11662.6, 11800.5, 11900.7,  # Multiple data points for the year 2005
        14270.7, 14300.8, 14500.9,  # Multiple data points for the year 2010
        17462.2, 17500.3, 17600.4,  # Multiple data points for the year 2015
        21367.4, 21400.5, 21500.6   # Multiple data points for the year 2020
    ],
    'year': [
        2000, 2000, 2000,  # Corresponding years
        2005, 2005, 2005,
        2010, 2010, 2010,
        2015, 2015, 2015,
        2020, 2020, 2020
    ]
})

# Function to create a violin plot with a squeezed base area
def create_violin_plot(data):
    chart = alt.Chart(data).transform_density(
        'population_sum',
        as_=['population_sum', 'density'],
        extent=[data.population_sum.min(), data.population_sum.max()],
        groupby=['year']
    ).mark_area(
        orient='horizontal',
        opacity=0.6
    ).encode(
        alt.X('density:Q', stack='center', axis=alt.Axis(labels=False, title=None)),
        alt.Y('population_sum:Q', scale=alt.Scale(zero=False)),
        color=alt.Color('year:N'),
        column=alt.Column('year:N', header=alt.Header(titleOrient='bottom', labelOrient='bottom', labelPadding=0))
    ).properties(
        width=100
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    )
    
    return chart

def app():
    st.title('Population Data Visualization')

    # Create and display the violin plot
    violin_plot = create_violin_plot(population_data)
    st.altair_chart(violin_plot, use_container_width=True)

if __name__ == '__main__':
    app()
