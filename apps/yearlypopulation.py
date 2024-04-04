import streamlit as st
import pandas as pd
import altair as alt

def app():
    st.title("Population Data Visualization")

    # Sample data, replace this with your actual DataFrame
    population_data = pd.DataFrame({
        'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
        'year': [2000, 2005, 2010, 2015, 2020]
    })

    # Create the violin plot using Altair
    violin_chart = alt.Chart(population_data).transform_density(
        'population_sum',
        as_=['population_sum', 'density'],
        extent=[population_data['population_sum'].min(), population_data['population_sum'].max()],
        groupby=['year']
    ).mark_area(orient='horizontal').encode(
        alt.Y('population_sum:Q', title='Population'),
        color='year:N',
        x=alt.X(
            'density:Q',
            stack='center',
            impute=None,
            title=None,
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True),
        ),
        column=alt.Column(
            'year:O',  # Changed to ordinal to treat the year as a discrete variable
            header=alt.Header(
                titleOrient='bottom',
                labelOrient='bottom',
                labelPadding=0,
            ),
        )
    ).properties(
        width=100,
        height=450
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    )

    # Display the violin plot in the Streamlit app
    st.altair_chart(violin_chart, use_container_width=True)

# Ensure to call the app function if this script is run standalone
if __name__ == "__main__":
    app()
