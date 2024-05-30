import streamlit as st
import leafmap.foliumap as leafmap

markdown = """
"A Streamlit Application for Active Mobility \n<https://active-mobility-bonaire-uci.streamlit.app/>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)


with col1:

    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)
    m.set_center(lat=12.15, lon=-68.26, zoom=12)  # Centering and zooming to Bonaire
    m.to_streamlit(height=700)


hide_github_icon = """
    <style>
        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, 
        .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, 
        .viewerBadge_text__1JaDK { display: none; } 
        #MainMenu { visibility: hidden; } 
        footer { visibility: hidden; } 
        header { visibility: hidden; }
    </style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)