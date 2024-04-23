import streamlit as st

def display_key_insights():
    st.header("Key Insights")
    st.markdown("""
        
        - **Income and Transportation Choices**: Not strong relationship showing a slight tendency towards both car usage and bicycle use with higher incomes.
        - **Gender and Mobility**: Mobility choices show very weak correlation with gender, suggesting similar behaviors across genders or that gender isn't a primary factor.
        - **Household Size and Transport**: Larger household sizes correlate negatively with car usage, suggesting economic influences on transport choices.
        - **Gender:** There's a very weak correlation between gender and other variables such as 'Car', 'Bicycle', and 'Travel'. This suggests that gender alone isn't a strong predictor of transportation preferences in this dataset.
        - **Agegroup:** There's a moderate positive correlation (0.31) between 'Agegroup' and 'Country', suggesting that age may be related to the country of the respondents, perhaps indicating a demographic trend where certain age groups might be tourists or expatriates. There's no strong correlation between age group and the modes of transport ('Car', 'Bicycle', 'Travel') which implies that age may not be a defining factor in how people choose to travel in Bonaire.
        - **Site:** The 'Site' variable has very weak to no correlation with 'Bicycle' and 'Travel', suggesting that the location within Bonaire may not significantly affect these aspects of mobility.
        - **Bicycle vs. Car:** There's a negative correlation (-0.39) between 'Bicycle' usage and 'Car' usage, which indicates that people who cycle more tend to use cars less. This is a key insight for policy as it suggests that improvements to bicycle infrastructure could reduce car dependency.
        - **Bicycle vs. Travel:** There's no strong correlation between 'Bicycle' and 'Travel', which may include various modes such as walking, public transport, etc. This lack of a strong relationship indicates that cycling habits might be independent of other travel preferences.
        - **Travel vs. Car:** The negative correlation (-0.41) between 'Travel' and 'Car' suggests that people who frequently use other modes of travel are less likely to use cars. This is consistent with what you'd expect if 'Travel' includes active travel modes.
    """)

def display_policy_recommendations():
    st.header("Policy Recommendations")
    st.markdown("""
        - **Demographic-Specific Mobility Programs**: Cater mobility programs to different demographic segments for better effectiveness.
        - **Active Mobility in High-Income Groups**: Introduce incentives for high-income individuals to adopt active travel modes.
        - **Infrastructure Investment**: Encourage cycling through robust infrastructure to decrease reliance on cars.
        - **Household-Centric Travel Solutions**: Create family-friendly travel options and subsidies for larger households.
        - **Country-Specific Mobility Strategies**: Consider cultural and economic contexts in mobility strategies.
    """)

def display_bold_statements():
    st.header("Bold Policy Statements")
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
