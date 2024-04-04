import altair as alt
import pandas as pd
import streamlit as st

# Sample population data
population_data = pd.DataFrame({
    'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
    'year': [2000, 2005, 2010, 2015, 2020]
})

# Function to create a violin plot with the given template
def create_violin_plot(data):
    chart = alt.Chart(data, width=100).transform_density(
        'population_sum',
        as_=['population_sum', 'density'],
        extent=[data.population_sum.min(), data.population_sum.max()],
        groupby=['year']
    ).mark_area(orient='horizontal').encode(
        alt.X('density:Q')
            .stack('center')
            .impute(None)
            .title(None)
            .axis(labels=False, values=[0], grid=False, ticks=True),
        alt.Y('population_sum:Q'),
        alt.Color('year:N'),
        alt.Column('year:N')
            .spacing(0)
            .header(titleOrient='bottom', labelOrient='bottom', labelPadding=0)
    ).configure_view(
        stroke=None
    )
    
    return chart

def app():
    st.title('Population Data Visualization')

    # Create and display the violin plot
    violin_plot = create_violin_plot(population_data)
    st.altair_chart(violin_plot, use_container_width=True)

# Run the app function if the script is executed
if __name__ == '__main__':
    app()
