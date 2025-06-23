import requests
import os
from io import BytesIO
from PIL import Image
import numpy as np
def get_bing_satellite_image(lat, lon, zoom=18, size='350,350', key='YOUR_BING_KEY'):
    url = f"https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/{lat},{lon}/{zoom}?mapSize={size}&key={key}"
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Error("Failed to download image")


def generate_grid_coordinates(center_lat, center_lon, steps=3, offset=0.001):
    '''
        This function generates grid structure from the center grid 
    '''
    lats = [center_lat + i * offset for i in range(-(steps//2), (steps//2)+1)]
    lons = [center_lon + i * offset for i in range(-(steps//2), (steps//2)+1)]
    grid = [(lat, lon) for lat in lats for lon in lons]
    return grid


def download_grid_images(center_lat: float,center_lon:float,key,save_dir:str):
    os.makedirs(save_dir,exist_ok=True)
    coords = generate_grid_coordinates(center_lat,center_lon)
    for i, (lat, lon) in enumerate(coords):
        img = get_bing_image(lat, lon, key=key)
        if img:
            img.save(f"{save_dir}/image_{i}_{lat}_{lon}.png")

