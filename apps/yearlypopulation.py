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

# Define the Streamlit app
def app():
    st.title("Population Data Visualization")

    # Sample population data with years and population sums
    population_data = pd.DataFrame({
        'population_sum': [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252],
        'year': [2000, 2005, 2010, 2015, 2020]
    })

    # Prepare the data for sunburst plot
    # Each year will be treated as a separate segment
    sunburst_data = {
        'names': population_data['year'].astype(str).tolist() + ["Population"],
        'parents': [""] + ["Population"] * population_data['year'].size,
        'values': [population_data['population_sum'].sum()] + population_data['population_sum'].tolist(),
    }

    # Create a sunburst plot
    sunburst_fig = px.sunburst(
        sunburst_data,
        names='names',
        parents='parents',
        values='values',
        color='values',
        color_continuous_scale='Blues',
    )

    # Update the layout for better margins and title
    sunburst_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title_text='Population over the Years')

    # Display the sunburst plot in Streamlit
    st.plotly_chart(sunburst_fig, use_container_width=True)

# Execute the app function when running the script
if __name__ == '__main__':
    app()


# Execute the app function when running the script
if __name__ == '__main__':
    app()

