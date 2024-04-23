import streamlit as st

def display_key_insights():
    st.header("Key Insights from Cross-Dataset Correlation Analysis")
    st.markdown("""
        - **Age and Geographic Correlations**: Potential demographic patterns with moderate correlation between age group and country.
        - **Car Usage vs. Active Travel**: Significant negative correlation suggests a trade-off between car use and engaging in active travel.
        - **Income and Transportation Choices**: Nuanced relationship showing a slight tendency towards both car usage and bicycle use with higher incomes.
        - **Gender and Mobility**: Mobility choices show very weak correlation with gender, suggesting similar behaviors across genders or that gender isn't a primary factor.
        - **Household Size and Transport**: Larger household sizes correlate negatively with car usage, suggesting economic or logistical influences on transport choices.
    """)

def display_policy_recommendations():
    st.header("Policy Recommendations for Enhancing Active Mobility")
    st.markdown("""
        - **Demographic-Specific Mobility Programs**: Cater mobility programs to different demographic segments for better effectiveness.
        - **Active Mobility in High-Income Groups**: Introduce incentives for high-income individuals to adopt active travel modes.
        - **Infrastructure Investment**: Encourage cycling through robust infrastructure to decrease reliance on cars.
        - **Household-Centric Travel Solutions**: Create family-friendly travel options and subsidies for larger households.
        - **Country-Specific Mobility Strategies**: Consider cultural and economic contexts in mobility strategies.
    """)

def display_bold_statements():
    st.header("Bold Policy Statements for Bonaire's Active Mobility")
    st.markdown("""
        - **"Creating a Bicycle-Friendly Bonaire"**: A robust cycling infrastructure will reduce car dependency.
        - **"Culturally Inclusive Active Mobility"**: Mobility solutions should respect and incorporate cultural differences.
        - **"Economic Incentives for Sustainable Transport"**: Financial benefits for sustainable transport can encourage a shift in high-income groups.
        - **"Family-Friendly Transportation"**: Develop practical transportation plans for larger households.
        - **"Data-Driven Mobility Enhancement"**: Policies should be responsive to the evolving needs of Bonaire's population.
    """)

def app():
    st.title("Active Mobility Data Insights and Policies")
    
    # Divide the page into two columns to display insights and policy recommendations side by side
    col1, col2 = st.columns(2)
    
    with col1:
        display_key_insights()
        
    with col2:
        display_policy_recommendations()
        
    # Display bold statements below the columns
    display_bold_statements()

if __name__ == "__main__":
    app()
