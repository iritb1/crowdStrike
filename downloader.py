import os
import requests
from bs4 import BeautifulSoup
from config import Constants, logger
from http import HTTPStatus
from typing import Optional

PROJECT_DIR: str = os.path.dirname(os.path.abspath(__file__))
TMP_DIR: str = os.path.join(PROJECT_DIR, "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

def download_image(animal_name: str, wikipedia_url: str) -> Optional[str]:
    """
    Downloads the first image from the Wikipedia page of the given animal.
    If no image is found in the infobox, it searches the main body content.
    """
    try:
        response = requests.get(f"https://en.wikipedia.org{wikipedia_url}")
        if response.status_code != HTTPStatus.OK:
            logger.error(f"Failed to fetch page for {animal_name}")
            return None

        soup: BeautifulSoup = BeautifulSoup(response.content, Constants.HTML_PARSER)

        #Try to find the image in the infobox
        infobox = soup.find("table", class_="infobox")
        
        #If no infobox is found, search in the main body content
        if not infobox:
            infobox = soup.find("div", class_="mw-body-content")

        #Finds the first image inside the selected section
        image_tag = infobox.find("img", class_="mw-file-element") if infobox else None

        if not image_tag:
            logger.warning(f"No suitable image found for {animal_name}")
            return None

        image_url: str = "https:" + image_tag["src"]
        image_ext: str = image_url.split(".")[-1].lower()  # Extract file extension
        
        #Sanitize filename to prevent directory issues
        safe_animal_name: str = animal_name.replace("/", "_")
        image_filename: str = f"{safe_animal_name}.{image_ext}"
        image_path: str = os.path.join(TMP_DIR, image_filename)

        if os.path.exists(image_path):
            logger.info(f"Image already downloaded: {image_filename}")
            return image_filename

        img_data: bytes = requests.get(image_url).content
        with open(image_path, "wb") as f:
            f.write(img_data)

        logger.info(f"Downloaded: {image_filename}")
        return image_filename
    except Exception as e:
        logger.error(f"Error downloading {animal_name}: {e}")
        return None
