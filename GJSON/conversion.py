import geopandas as gpd
import os

def convert_shapefiles_to_geojson(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".shp"):
            # Construct the full file path
            filepath = os.path.join(input_folder, file)
            # Load the Shapefile into a GeoDataFrame
            gdf = gpd.read_file(filepath)
            # Construct the output file path
            output_file_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.geojson')
            # Save the GeoDataFrame as a GeoJSON file
            gdf.to_file(output_file_path, driver='GeoJSON')
            print(f"Converted {file} to GeoJSON.")

# Use the specific paths you provided
input_folder = r'C:\Users\Gebruiker\Desktop\My Lab\University of Amsterdam_UCI\Bonaire\Bought\data'
output_folder = r'C:\Users\Gebruiker\Desktop\My Lab\University of Amsterdam_UCI\Bonaire\GJSON'

convert_shapefiles_to_geojson(input_folder, output_folder)
