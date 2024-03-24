import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, climate  # Import your app modules here

st.set_page_config(page_title="Bonaire Geospatial", layout="wide")

# Define your apps and their titles and icons
apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": climate.app, "title": "Climate Analysis", "icon": "cloud"},
]

# Generate lists of titles and icons for the sidebar menu
titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

# Sidebar menu
with st.sidebar:
    selected = option_menu("Main Menu", titles, icons=icons, menu_icon="cast", default_index=0)

# Render the selected app
for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
