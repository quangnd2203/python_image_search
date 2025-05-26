import os
import requests
from duckduckgo_search import DDGS
from PIL import Image
from io import BytesIO

def download_images(query, out_dir="dataset", max_results=50):
    os.makedirs(f"{out_dir}/{query}", exist_ok=True)
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=max_results)

        for i, result in enumerate(results):
            url = result["image"]
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    # Verify the file is a valid image
                    image = Image.open(BytesIO(r.content)).convert("RGB")

                    filename = f"{out_dir}/{query}/{query.replace(' ', '_')}_{i}.jpg"
                    image.save(filename, "JPEG")
            except Exception as e:
                print(f"⚠️ Skipped {url}: {e}")

download_images("only left arm person")
download_images("only right arm person")