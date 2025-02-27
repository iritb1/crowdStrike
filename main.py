from scraper import get_adjectives_with_animals
from html_generator import generate_html

def main():
    url = "https://en.wikipedia.org/wiki/List_of_animal_names"
    
    #Scrape data and download images
    adj_to_animals, animal_image_map = get_adjectives_with_animals(url)
    
    #Generate HTML file
    html_content = generate_html(adj_to_animals, animal_image_map)
    output_file = "collateral_adjectives.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file generated: {output_file}")

if __name__ == "__main__":
    main()
