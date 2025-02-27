import requests
import threading
import re
from bs4 import BeautifulSoup
from http import HTTPStatus
from collections import defaultdict
from downloader import download_image
from typing import Dict, Set, Tuple
from config import Constants

def extract_adjectives(text: str) -> set[str]:
    """Extract individual adjectives from a collateral adjective cell."""
    cleaned = re.sub(Constants.REMOVE_PARENTHESIS_REGEX, ' ', text)
    cleaned = re.sub(Constants.REMOVE_BRACKETS_REGEX, ' ', cleaned)
    parts = re.split(Constants.SPLIT_OR_REGEX, cleaned, flags=re.IGNORECASE)
    return [word.lower() for part in parts for word in re.findall(Constants.WORD_EXTRACTION_REGEX, part)]

def extract_animal(text: str) -> str:
    """Cleans an animal cell text."""
    cleaned = re.sub(Constants.REMOVE_PARENTHESIS_REGEX, '', text)
    cleaned = re.sub(Constants.REMOVE_BRACKETS_REGEX, '', cleaned)
    return re.split(Constants.REMOVE_ALSO_SEE_REGEX, cleaned, flags=re.IGNORECASE)[0].strip()

def get_adjectives_with_animals(url: str) -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    """Scrapes Wikipedia and maps collateral adjectives to animals (only if adjectives exist)."""
    response = requests.get(url)
    if response.status_code != HTTPStatus.OK:
        raise Exception(f"Error fetching page: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    adj_to_animals: Dict[str, Set[str]] = defaultdict(set)
    tables = soup.find_all('table', class_='wikitable')
    if len(tables) < 2:
        raise Exception("Expected at least two tables, but found fewer.")

    table = tables[1]
    header_row = table.find('tr')
    if not header_row:
        return adj_to_animals

    headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
    headers_lower = [h.lower() for h in headers]

    coll_index, animal_index = headers_lower.index("collateral adjective"),  headers_lower.index("animal")

    if coll_index is None or animal_index is None:
        return adj_to_animals

    download_threads = []
    animal_image_map: Dict[str, str] = {}

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) <= max(coll_index, animal_index):
            continue

        coll_text = cells[coll_index].get_text(" ", strip=True)
        animal_text = cells[animal_index].get_text(" ", strip=True)
        a_tag = cells[animal_index].find('a')
        wikipedia_link = a_tag['href'] if a_tag else None

        if coll_text and animal_text and wikipedia_link:
            cleaned_animal = extract_animal(animal_text)
            if not cleaned_animal:
                continue

            #Extract collateral adjectives from the collateral adjective cell.
            adjectives = extract_adjectives(coll_text)
            #Process only if at least one adjective is found.
            if not adjectives:
                continue

            for adj in filter(None, extract_adjectives(coll_text)):
                adj_to_animals[adj].add(cleaned_animal)

            #Download image in a separate thread.
            thread = threading.Thread(
                target=lambda: animal_image_map.update({
                    cleaned_animal: download_image(cleaned_animal, wikipedia_link)
                })
            )
            thread.start()
            download_threads.append(thread)

    #Wait for all download threads to finish.
    for thread in download_threads:
        thread.join()

    return adj_to_animals, animal_image_map
