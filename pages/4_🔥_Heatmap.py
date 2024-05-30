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

#st.title("Heatmap")

with st.expander("See source code"):
    #with st.echo():
        filepath = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        m = leafmap.Map(center=[40, -100], zoom=4)
        m.set_center(lat=12.15, lon=-68.26, zoom=12)  # Centering and zooming to Bonaire
        m.add_heatmap(
            filepath,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=20,
        )
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