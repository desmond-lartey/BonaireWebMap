import folium
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Example list of neighborhoods with manually approximated central points (latitude, longitude)
neighborhoods_info = [
    {"name": "Playa", "location": (12.1500, -68.2767)},
    # Add other neighborhoods with their approximate central locations
]

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(neighborhoods_info)

# Convert central points to geometric points and buffer to create approximate areas
gdf['geometry'] = gdf.apply(lambda row: Point(row['location'][1], row['location'][0]).buffer(0.005), axis=1)  # Adjust buffer as necessary

# Initialize a folium map centered on Bonaire
m = folium.Map(location=[12.15, -68.27], zoom_start=11)

# Add neighborhood areas to the map
for _, row in gdf.iterrows():
    folium.GeoJson(row['geometry'], tooltip=row['name']).add_to(m)

# Display the map in Streamlit
m._to_html()
