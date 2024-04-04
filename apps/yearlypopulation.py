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

    # Convert year to string to be used as a categorical variable for treemap path
    population_data['year'] = population_data['year'].astype(str)

    # Create a treemap
    fig = px.treemap(population_data, 
                     path=['year'], 
                     values='population_sum', 
                     color='population_sum',
                     color_continuous_scale='Blues')

    # Update the layout for better margins and title
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title_text='Population by Year')

    # Display the treemap in Streamlit
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import plotly.express as px
import pandas as pd

# Treemap chart function
def get_treemap():
    population_data = pd.DataFrame({
        'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
        'year': [2000, 2005, 2010, 2015, 2020]
    })
    population_data['year'] = population_data['year'].astype(str)
    fig = px.treemap(
        population_data, 
        path=['year'], 
        values='population_sum', 
        color='population_sum',
        color_continuous_scale='Blues'
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title_text='Population by Year')
    return fig

# Sunburst chart function
@st.experimental_memo
def get_sunburst():
    data = dict(
        character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
        value=[10, 14, 12, 10, 2, 6, 6, 4, 4]
    )
    fig = px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value',
    )
    return fig

# Streamlit app
def app():
    st.title("Population Data Visualization")

    # Treemap
    treemap_fig = get_treemap()
    st.plotly_chart(treemap_fig, use_container_width=True)

    # Sunburst
    st.write("Sunburst Chart")
    sunburst_fig = get_sunburst()

    # Tabs for different themes
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(sunburst_fig, theme="streamlit")
    with tab2:
        st.plotly_chart(sunburst_fig, theme=None)

# Execute the app function when running the script
if __name__ == '__main__':
    app()

# Execute the app function when running the script
if __name__ == '__main__':
    app()

