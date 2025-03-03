# building a buffer shape for filtering the weather data
import geopandas
from shapely.ops import unary_union

city = geopandas.read_file("../assets/magdeburg.shp")

city = city.to_crs("epsg:3857")
berlin_boundary = geopandas.GeoDataFrame(
    geopandas.GeoSeries(unary_union(city["geometry"]))
)
berlin_boundary = berlin_boundary.rename(columns={0: "geometry"}).set_geometry(
    "geometry"
)

city_buffer = berlin_boundary.buffer(2000)
city_buffer = city_buffer.simplify(1000)

city_buffer = geopandas.GeoDataFrame(city_buffer)
city_buffer = city_buffer.rename(columns={0: "geometry"}).set_geometry("geometry")
city_buffer.crs = "epsg:3857"
city_buffer.to_file("../assets/buffer.shp")
