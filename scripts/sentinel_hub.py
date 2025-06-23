from datetime import datetime, timedelta
from sentinelhub import SHConfig, BBox, CRS, bbox_to_dimensions, SentinelHubRequest, DataCollection, MimeType
import os
import numpy as np
from PIL import Image
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

load_dotenv()
config = SHConfig()
config.sh_client_id = os.getenv("CLIENT_ID")
config.sh_client_secret = os.getenv("CLIENT_SECRET")
if not config.sh_client_id or not config.sh_client_secret:
    raise ValueError("Missing SentinelHub credentials")

# Set Vienna location (frequent coverage)
lat, lon = 48.2082, 16.3738
bbox = BBox([lon-0.005, lat-0.005, lon+0.005, lat+0.005], crs=CRS.WGS84)
size = bbox_to_dimensions(bbox, resolution=10)

# Evalscript: raw RGB bands, no mask
evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B04", "B03", "B02"],
    output: { bands: 3 },
    mosaicking: "ORBIT"
  };
}
function evaluatePixel(sample) {
  return [
    sample.B04 / 10000.0,
    sample.B03 / 10000.0,
    sample.B02 / 10000.0
  ];
}
"""

# Set time range to known recent availability
time_interval = ("2024-06-01", "2024-06-10")

# Request
request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=time_interval,
            maxcc=1.0  # Accept all cloud cover for now
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    bbox=bbox,
    size=size,
    config=config
)

try:
    image = request.get_data()[0]
    print(f"Image shape: {image.shape}, min: {image.min()}, max: {image.max()}, mean: {image.mean()}")

    image = np.clip(image, 0, 1)
    img_8bit = (image * 255).astype(np.uint8)

    os.makedirs("images", exist_ok=True)
    filename = "images/test_image_vienna.png"
    Image.fromarray(img_8bit).save(filename)
    print(f"✅ Saved image to: {filename}")

    plt.imshow(image)
    plt.title("Vienna RGB (Sentinel-2)")
    plt.savefig("images/preview.png")
    plt.close()
except Exception as e:
    print(f"Error: {e}")
