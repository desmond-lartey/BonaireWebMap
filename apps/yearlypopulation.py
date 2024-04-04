import streamlit as st
import plotly.express as px
import pandas as pd

# Define the Streamlit app
def app():
    st.title("Population Data Visualization")

    # Sample population data with years and population sums
    population_data = pd.DataFrame({
        'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
        'year': [2000, 2005, 2010, 2015, 2020]
    })

    # Treemap visualization
    population_data['year_str'] = population_data['year'].astype(str)  # For treemap path
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
        title="Population Scatter Plot over Years"
    )
    scatter_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # Display the scatter plot in Streamlit with tabs for themes
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(scatter_fig, theme="streamlit")
    with tab2:
        st.plotly_chart(scatter_fig, theme=None)

# Run the Streamlit app
if __name__ == '__main__':
    app()
