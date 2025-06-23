from datetime import datetime, timedelta
from sentinelhub import SHConfig, BBox, CRS, bbox_to_dimensions, SentinelHubRequest, DataCollection, MimeType
from dotenv import load_dotenv
import os
import cv2
from PIL import Image
load_dotenv()
config = SHConfig()
config.sh_client_id = os.getenv("CLIENT_ID")
config.sh_client_secret = os.getenv("CLIENT_SECRET")
LAT, LON = 8.9806, 38.7578  # Addis Ababa
RADIUS = 300  # meters (~1000 ft)
RESOLUTION = 10  # meters/pixel

bbox = BBox(
    bbox=[LON - 0.005, LAT - 0.005, LON + 0.005, LAT + 0.005],
    crs=CRS.WGS84
)
size = bbox_to_dimensions(bbox, resolution=RESOLUTION)

# --------------------------- Multiple Date Requests ---------------------------
start_date = datetime(2024, 6, 1)
end_date = datetime(2024, 6, 10)
time_step = 5

date_list = [start_date + timedelta(days=i) for i in range(0, (end_date - start_date).days + 1, time_step)]

images = []
evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B04", "B03", "B02"],
    output: { bands: 3 }
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

for date in date_list:
    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=(date.strftime('%Y-%m-%dT%H:%M:%S'), (date + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S'))
            )
        ],
        responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=config
    )
    image = request.get_data()[0]
    images.append(image)
def save_images_to_directory(images, directory, prefix="image"):
    os.makedirs(directory, exist_ok=True)
    for idx, img in enumerate(images):
        img_8bit = (img * 255).astype('uint8')
        im = Image.fromarray(img_8bit, 'RGB')
        filename = os.path.join(directory, f"{prefix}_{idx+1}.png")
        im.save(filename)
if __name__ == '__main__':
    save_images_to_directory(images,'../datasets')