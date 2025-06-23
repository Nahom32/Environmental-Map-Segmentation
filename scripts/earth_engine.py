import ee
import geemap
import os

# Initialize Earth Engine
ee.Initialize()

# Define location and parameters
center = [11.57628, 37.42476]
radius = 3048  # meters
geometry = ee.Geometry.Point(center[1], center[0]).buffer(radius)
output_dir = os.path.expanduser('~/sentinel_output')  # Output directory

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Fetch Sentinel-2 collection
collection = ee.ImageCollection('COPERNICUS/S2').filterBounds(geometry).filterDate('2025-05-01', '2025-05-10').filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    
# Check if images exist
if collection.size().getInfo() == 0:
    print("No suitable images found.")
    exit()

# Get the first image
image = ee.Image(collection.first())
print("Image ID:", image.id().getInfo())

# 1. Export raw spectral bands (B2, B3, B4) as GeoTIFF
raw_filename = os.path.join(output_dir, 'sentinel_raw.tif')
geemap.ee_export_image(
    image.select(['B2', 'B3', 'B4']),
    filename=raw_filename,
    scale=10,
    region=geometry,
    file_per_band=False
)
print(f"Raw bands saved to {raw_filename}")

# 2. Export visualized RGB as GeoTIFF
vis_params = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 3000,
    'gamma': 1.4
}
rgb_filename = os.path.join(output_dir, 'sentinel_rgb.tif')
geemap.ee_export_image(
    image.visualize(**vis_params),
    filename=rgb_filename,
    scale=10,
    region=geometry
)
print(f"RGB image saved to {rgb_filename}")

# 3. Optional: Export as PNG (without georeferencing)
png_filename = os.path.join(output_dir, 'sentinel_rgb.png')
geemap.ee_export_image_to_drive(
    image.visualize(**vis_params),
    description='SentinelExport',
    folder='EarthEngine',
    region=geometry,
    scale=10,
    file_format='PNG'
)
print(f"PNG export started. Check Google Drive folder 'EarthEngine' for {png_filename}")