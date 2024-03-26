# apps/home.py
import streamlit as st


def app():
    st.title("Home")
    st.markdown("Welcome to the Bonaire Interactive Map Portal.")

    st.header("Enhancing Active Mobility in Bonaire")
    st.markdown("""
    In recent years, global initiatives have emphasized the need to increase physical activity levels, especially through walking and cycling, to improve public and planetary health. The Caribbean Dutch municipality of Bonaire is embarking on an ambitious project to enhance active mobility and promote health equity among its residents.
    
    This effort, supported by the Netherlands’ Ministry of Public Health, involves a multidisciplinary team including researchers from the Urban Cycling Institute, local government staff, and key stakeholders on the island. A pivotal aim is to integrate physical activity into daily life, combatting obesity and related health conditions prevalent in the region.
    """)

    st.image("https://www.example.com/path-to-bonaire-image.jpg", caption="Bonaire - Enhancing Active Mobility")

    st.subheader("Project Goals")
    st.markdown("""
    - **Increase Physical Activity**: Focusing on integrating walking and cycling into the daily routines of Bonaire's residents.
    - **Health Equity**: Address obesity, mortality, and morbidity through active mobility.
    - **Community Involvement**: Employ community-based participatory research to ensure policy actions are developed for Bonaire, by Bonaire.
    """)

    st.subheader("Contact Information")
    st.markdown("""
    For more information about the project or to get involved, please contact:
    
    **Dr. Dylan Power**  
    Senior Researcher, Urban Cycling Institute  
    Email: [dylan@urbancyclinginstitute.org](mailto:dylan@urbancyclinginstitute.org)
    
    **Rita Gemerts**  
    Embedded Citizen Scientist, Ray-Action  
    """)
    
    st.sidebar.info(
        """
        **Web App URL**: [https://streamlit.geemap.org](https://streamlit.geemap.org)  
        **GitHub repository**: [https://github.com/giswqs/streamlit-geospatial](https://github.com/giswqs/streamlit-geospatial)
        """
    )

    st.sidebar.title("Contact")
    st.sidebar.markdown(
        """
        **Urban Cycling Institute**  
        [Read more](https://urbancyclinginstitute.org/enhancing-active-mobility-on-bonaire/)  
        [Education](https://urbancyclinginstitute.org/education/) | [Events](https://urbancyclinginstitute.org/events/) | [Projects](https://urbancyclinginstitute.org/projects/) | [LinkedIn](https://www.linkedin.com/company/urbancyclinginstitute/)
        """
    )

    st.markdown(
        """
        This multi-page web app demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and open-source mapping libraries, 
        such as [leafmap](https://leafmap.org), [geemap](https://geemap.org), [pydeck](https://deckgl.readthedocs.io), and [kepler.gl](https://docs.kepler.gl/docs/keplergl-jupyter).
        """
    )

    st.info("Click on the left sidebar menu to navigate to the different apps.")

    st.subheader("Timelapse of Satellite Imagery")
    st.markdown(
    """
    The following timelapse animations were created using the Timelapse web app. Click `Timelapse` on the left sidebar menu to create your own timelapse for any location around the globe.
"""
)

    import datetime

    current_year = datetime.datetime.now().year
    st.sidebar.markdown(f"© {current_year} Copyright Urban Cycling Institute")

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.image("https://github.com/giswqs/data/raw/main/timelapse/spain.gif")
        st.image("https://github.com/giswqs/data/raw/main/timelapse/las_vegas.gif")

    with row1_col2:
        st.image("https://github.com/giswqs/data/raw/main/timelapse/goes.gif")
        st.image("https://github.com/giswqs/data/raw/main/timelapse/fire.gif")