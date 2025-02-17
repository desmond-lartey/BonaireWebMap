import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, findings, facilities, popdashboard2, yearlypopulation, statistics #newpopdashboard, #area  # Make sure to import your app modules here

# import streamlit as st
# from streamlit_option_menu import option_menu
# from apps import home, facilities, neighbourhoods

# Setting up the page configuration
st.set_page_config(page_title="Bonaire Geospatial", layout="wide")

# Defining the apps and their titles and icons
apps = [
    {"func": home.app, "title": "Home"},
    {"func": facilities.app, "title": "Facilities"},
    {"func": popdashboard2.app, "title": "Population by Age_Sex"},
    #{"func": newpopdashboard.app, "title": "General dashboard", "icon": "bar_chart"},
    {"func": yearlypopulation.app, "title": "Population by Area"},
    {"func": statistics.app, "title": "Field Observation"},
    {"func": findings.app, "title": "Insights"}
]

# Creating the sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # The title of the menu
        options=[app["title"] for app in apps],  # The list of options
        icons=[app["icon"] for app in apps],  # The list of icons
        menu_icon="cast",  # The icon of the menu
        default_index=0,  # The default option selected
    )

# Displaying the selected app
for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
