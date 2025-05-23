# building a buffer shape for filtering the weather data
import geopandas
import os
from shapely.ops import unary_union

input_path = os.getenv("SURROUNDING_SHAPE_FILE")
if input_path is None:
    raise ValueError("Environment variable SURROUNDING_SHAPE_FILE is not set.")

if not os.path.exists(input_path):
    raise FileNotFoundError(
        f"Input shapefile not found at path: {input_path}. "
        f"Please check the SURROUNDING_SHAPE_FILE environment variable."
    )

city = geopandas.read_file(input_path)

# Get the directory of the input file
input_dir = os.path.dirname(input_path)
# Define the output filename
output_filename = "buffer.shp"
# Construct the full output path
output_path = os.path.join(input_dir, output_filename)

city = city.to_crs("epsg:3857")
city_boundary = geopandas.GeoDataFrame(
    geopandas.GeoSeries(unary_union(city["geometry"]))
)
city_boundary = city_boundary.rename(columns={0: "geometry"}).set_geometry(
    "geometry"
)

city_buffer = city_boundary.buffer(2000)
city_buffer = city_buffer.simplify(1000)

berlin_buffer = geopandas.GeoDataFrame(city_buffer)
berlin_buffer = berlin_buffer.rename(columns={0: "geometry"}).set_geometry("geometry")
berlin_buffer.crs = "epsg:3857"
berlin_buffer.to_file(output_path)
