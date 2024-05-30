# apps/home.py
import streamlit as st
import leafmap.foliumap as leafmap
import datetime

# Set the page configuration
st.set_page_config(layout="wide")

# Customize the sidebar
st.sidebar.title("About")
st.sidebar.info("A Streamlit Application for Active Mobility \n<https://active-mobility-bonaire-uci.streamlit.app/>")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Page Title

# Home Page Content
st.header("Enhancing Active Mobility in Bonaire")
st.markdown("""
In recent years, global initiatives have emphasized the need to increase physical activity levels, especially through walking and cycling, to improve public and planetary health. The Caribbean Dutch municipality of Bonaire wants to enhance active mobility and promote health equity among its residents.

This effort, supported by the Netherlands’ Ministry of Public Health, involves a multidisciplinary team including researchers from the Urban Cycling Institute, local government staff, and key stakeholders on the island. The objective is to integrate physical activity into daily life, addressing all related health conditions prevalent in the region.
""")
st.image("https://urbancyclinginstitute.org/wp-content/uploads/2024/01/active-mobility-Bonaire.jpeg", caption="Bonaire")

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

st.sidebar.info("""
[**Web App URL**]: (https://active-mobility-bonaire-uci.streamlit.app/)  
[**GitHub repository**]: (https://github.com/desmond-lartey/BonaireWebMap)
""")

st.sidebar.title("Contact")
st.sidebar.markdown("""
**Urban Cycling Institute**  
[Read Documentation of this App](https://github.com/desmond-lartey/BonaireWebMap?tab=readme-ov-file)  
[Education](https://urbancyclinginstitute.org/education/) | [Events](https://urbancyclinginstitute.org/events/) | [Project](https://urbancyclinginstitute.org/enhancing-active-mobility-on-bonaire/) | [LinkedIn](https://www.linkedin.com/company/urbancyclinginstitute/)
""")

st.info("Click on the left sidebar menu to navigate to the different apps.")

st.subheader("Timelapse of Satellite Imagery")

current_year = datetime.datetime.now().year
st.sidebar.markdown(f"© {current_year} Urban Cycling Institute")

# row1_col1, row1_col2 = st.columns(2)
# with row1_col1:
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/spain.gif")
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/las_vegas.gif")

# with row1_col2:
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/goes.gif")
#     st.image("https://github.com/giswqs/data/raw/main/timelapse/fire.gif")

# Instructions
st.header("Instructions")
st.markdown("""
1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.
""")

# Add map
m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
