import logging
import os


class Constants:
    HTML_PARSER = "html.parser"
    TMP_DIR = "tmp"
    BASE_URL = "https://en.wikipedia.org"
    ANIMAL_NAMES_URL = f"{BASE_URL}/wiki/List_of_animal_names"
    REMOVE_PARENTHESIS_REGEX = r'\([^)]*\)'  
    REMOVE_BRACKETS_REGEX = r'\[[^\]]*\]' 
    SPLIT_OR_REGEX = r'\s+or\s+'
    REMOVE_ALSO_SEE_REGEX = r'\balso see\b' 
    WORD_EXTRACTION_REGEX = r'\b[a-zA-Z]+\b' 

os.makedirs(Constants.TMP_DIR, exist_ok=True)

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
