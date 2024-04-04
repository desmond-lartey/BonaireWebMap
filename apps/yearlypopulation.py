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




import plotly.express as px
import pandas as pd

def create_sunburst_chart(years, population):
    # Create a DataFrame from the years and population data
    df = pd.DataFrame({'year': years, 'population_sum': population})

    # Add a root node for the sunburst chart
    df = df.append({'year': 'Total', 'population_sum': df['population_sum'].sum()}, ignore_index=True)

    # Setup parent-child relationship
    df['parent'] = 'Total'
    df.at[df['year'] == 'Total', 'parent'] = ''

    # Create the sunburst chart
    fig = px.sunburst(
        df,
        names='year',
        parents='parent',
        values='population_sum',
        color='population_sum',
        color_continuous_scale='Blues',
    )

    # Update layout for margins
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    return fig

# Usage
years = [2000, 2005, 2010, 2015, 2020]
population = [9531.10755, 11662.60621, 14270.78473, 17462.24582, 21367.43252]

    # Inside your Streamlit app, after creating the treemap
st.write("Sunburst Chart of Population by Year")
st.plotly_chart(sunburst_fig, use_container_width=True)

# Create the sunburst chart
sunburst_fig = create_sunburst_chart(years, population)

# Execute the app function when running the script
if __name__ == '__main__':
    app()

