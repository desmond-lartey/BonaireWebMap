# apps/facilities.py
import streamlit as st
import geemap.foliumap as geemap
import geopandas as gpd
import os
from branca.element import Template, MacroElement

def app():
    st.title("Facilities and Land Uses")

    # Sidebar for base map selection using geemap's basemaps
    basemap_choice = st.sidebar.selectbox(
        "Choose a basemap:",
        list(geemap.basemaps.keys()),
        index=list(geemap.basemaps.keys()).index("OpenStreetMap")  # Default to HYBRID
    )

    # Initialize the map with the selected basemap
    #m = geemap.Map(center=[12.15, -68.27], zoom=11, basemap=geemap.basemaps[basemap_choice])
    # Use a known working basemap as a string directly
    m = geemap.Map(center=[12.15, -68.27], zoom=14, basemap='OpenStreetMap')


    # Function to add a shapefile layer
    def add_shapefile_layer(shapefile_path, layer_name):
        # Ensure the shapefile path exists
        if os.path.exists(shapefile_path):
            # Read the shapefile
            gdf = gpd.read_file(shapefile_path)
            
            # Add the GeoDataFrame to the map
            m.add_gdf(gdf, layer_name=layer_name, zoom_to_layer=True)
        else:
            st.error(f"Shapefile not found at {shapefile_path}")

    # Dynamically construct the path to the shapefile
    base_path = os.path.dirname(__file__)  # Directory of this script
    project_root = os.path.join(base_path, os.pardir)  # Move up to the project root
    shapefile_path = os.path.join(project_root, "newlyexportedshp", "bonaireboundary.shp")
    add_shapefile_layer(shapefile_path, "Bonaire Boundary")
    shapefile_path = os.path.join(project_root, "newlyexportedshp", "bonairehexgrid.shp")
    add_shapefile_layer(shapefile_path, "Neighbourhoods")
    shapefile_path = os.path.join(project_root, "newlyexportedshp", "zonalstats.shp")
    add_shapefile_layer(shapefile_path, "Zonalstats")

    # Define the legend
    # legend_colors = {
    #     "Agricultural": "green",
    #     "Urban": "red",
    #     "Water": "blue",
    #     "Forest": "darkgreen",
    #     "Barren": "gray"
    # }
    # legend_title = "Land Use Types"

    # # Function to add a legend to the map
    # def add_legend(m, legend_title, legend_colors):
    #     template = """
    #     {{% macro html(this, kwargs) %}}
    #     <div style="position: fixed; 
    #                 bottom: 50px; left: 50px; width: 150px; height: 90px; 
    #                 background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
    #                 ">&nbsp; <b>{legend_title}</b> <br>
    #                 {{%- for label, color in legend_colors.items() %}}
    #                 &nbsp; <i class="fa fa-square fa-2x" style="color:{{{{color}}}}"></i> {{{{label}}}}<br>
    #                 {{%- endfor %}}
    #     </div>
    #     {{% endmacro %}}
    #     """

    #     macro = MacroElement()
    #     macro._template = Template(template.format(legend_title=legend_title, legend_colors=json.dumps(legend_colors)))

    #     m.get_root().add_child(macro)

    # Add the legend to the map
    #add_legend(m, legend_title, legend_colors)

    # Display the map
    m.to_streamlit(height=700)