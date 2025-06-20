import requests
import os
from io import BytesIO
from PIL import Image
def get_bing_satellite_image(lat, lon, zoom=18, size='350,350', key='YOUR_BING_KEY'):
    url = f"https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/{lat},{lon}/{zoom}?mapSize={size}&key={key}"
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Error("Failed to download image")


