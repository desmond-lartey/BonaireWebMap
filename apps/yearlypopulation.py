import altair as alt
import pandas as pd
import streamlit as st

# Sample population data
population_data = pd.DataFrame({
    'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
    'year': [2000, 2005, 2010, 2015, 2020]
})

# Function to create a horizontal violin plot
def create_violin_plot(data):
    chart = alt.Chart(data).mark_area(
        orient='vertical',  # Orientation is now vertical
        opacity=0.6
    ).encode(
        alt.X('year:O', title='Year'),  # Treat 'year' as an ordinal variable for discrete x-axis
        alt.Y('population_sum:Q', title='Population'),
        color='year:N'
    ).properties(
        width=600,
        height=300
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )
    
    return chart

def app():
    st.title('Population Data Visualization')

    # Create and display the violin plot
    violin_plot = create_violin_plot(population_data)
    st.altair_chart(violin_plot, use_container_width=True)

# Call the app function
if __name__ == '__main__':
    app()
