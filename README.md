Wikipedia Animal Names Scraper-
This project scrapes Wikipedia for a list of animal names and their collateral adjectives, downloads images for each animal, and generates a formatted HTML file displaying the results.

Features-

- Scrapes animal names and collateral adjectives from Wikipedia
- Downloads the first image from each animal's Wikipedia page
- Generates a styled HTML file with:
  - A table listing each collateral adjective and its associated animals
  - Clickable animal names that link to their downloaded images
- Uses multi-threading for efficient image downloading
- Includes unit tests to ensure reliability

Prerequisites-

- Ensure you have Python 3.7+ installed on your system.
- pip install requests beautifulsoup4 jinja2 pytest

Usage-

- Run the project using: python main.py

This will-

- Scrape Wikipedia for animal names and adjectives
- Download animal images
- Generate an HTML file (collateral_adjectives.html) in the project directory
- After running, open collateral_adjectives.html in your browser to view the results.

Running Tests-

- python -m pytest tests/test_scraper.py
- python -m pytest tests/test_generate_html.py

How It Works-
Scraper (scraper.py)- 1. Fetches the Wikipedia page containing animal names 2. Extracts collateral adjectives (e.g., "canine" → "Dog") 3. Uses regex filtering to clean the extracted text 4. Finds animal links and sends them for image downloading

    Image Downloader (downloader.py)-
        1. Extracts the first image from each animal's Wikipedia page
        2. Handles missing images gracefully (logs a warning)
        3. Stores images in the /tmp/ folder

    HTML Generator (html_generator.py)-
        1. Formats the extracted data into a styled HTML table
        2. Creates links to the downloaded images
        3. Ensures the output is clean and readable
