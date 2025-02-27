from html_generator import generate_html

def test_generate_html() -> None:
    """Test that `generate_html()` correctly formats an HTML table with animal data."""
    
    adj_to_animals = {
        "canine": {"Dog"},
        "feline": {"Cat"}
    }
    animal_image_map = {
        "Dog": "dog.jpg",
        "Cat": "cat.jpg"
    }

    html_output = generate_html(adj_to_animals, animal_image_map)

    #Ensure generated HTML contains correct table structure
    assert "<table>" in html_output
    assert "canine" in html_output
    assert "feline" in html_output
    assert '<a href="tmp/dog.jpg">Dog</a>' in html_output 
    assert '<a href="tmp/cat.jpg">Cat</a>' in html_output 
