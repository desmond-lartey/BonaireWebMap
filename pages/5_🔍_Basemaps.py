import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit Application for Active Mobility \n<https://active-mobility-bonaire-uci.streamlit.app/>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.title("Searching Basemaps")
st.markdown(
    """
This app is a demonstration of searching and loading basemaps from [xyzservices](https://github.com/geopandas/xyzservices) and [Quick Map Services (QMS)](https://github.com/nextgis/quickmapservices). Selecting from 1000+ basemaps with a few clicks.
"""
)

with st.expander("See demo"):
    st.image("https://i.imgur.com/0SkUhZh.gif")

row1_col1, row1_col2 = st.columns([3, 1])
width = None
height = 800
tiles = None

with row1_col2:

    checkbox = st.checkbox("Search Quick Map Services (QMS)")
    keyword = st.text_input("Enter a keyword to search and press Enter:")
    empty = st.empty()

    if keyword:
        options = leafmap.search_xyz_services(keyword=keyword)
        if checkbox:
            options = options + leafmap.search_qms(keyword=keyword)

        tiles = empty.multiselect("Select XYZ tiles to add to the map:", options)

    with row1_col1:
        m = leafmap.Map()

        if tiles is not None:
            for tile in tiles:
                m.add_xyz_service(tile)
        m.set_center(lat=12.15, lon=-68.26, zoom=12)  # Centering and zooming to Bonaire
        m.to_streamlit(width, height)


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