import ee
import folium
import geemap
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import rasterio
ee.Initialize()
center = [11.57628,37.42476]  # Latitude, Longitude
radius = 3048  # Radius in meters


geometry = ee.Geometry.Point(center[1], center[0]).buffer(radius)


collection = ee.ImageCollection('COPERNICUS/S2') \
    .filterBounds(geometry) \
    .filterDate('2024-05-01', '2024-05-10')  \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))  # Filter for low cloud cover


collection_size = collection.size().getInfo()
