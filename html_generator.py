from jinja2 import Template
from typing import Dict

def generate_html(adj_to_animals: Dict[str, set], animal_image_map: Dict[str, str]) -> str:
    """
    Generates an HTML file using Jinja2.

    Each row corresponds to one collateral adjective with all its associated animals listed (each on a new line).
    Animal names are clickable links to their downloaded image if available.
    """
    template = Template("""
    <html>
    <head>
        <meta charset='UTF-8'>
        <title>Collateral Adjectives and Animals</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
            th { background-color: #f2f2f2; text-align: left; }
        </style>
    </head>
    <body>
        <h1>Collateral Adjectives and their Associated Animals</h1>
        <table>
            <tr>
                <th>Collateral Adjective</th>
                <th>Animals</th>
            </tr>
            {% for adj, animals in adj_to_animals.items()|sort %}
                <tr>
                    <td>{{ adj }}</td>
                    <td>
                        {% for animal in animals|sort %}
                            {% if animal in animal_image_map and animal_image_map[animal] %}
                                <a href="tmp/{{ animal_image_map[animal] }}">{{ animal }}</a><br>
                            {% else %}
                                {{ animal }}<br>
                            {% endif %}
                        {% endfor %}
                    </td>
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """)
    return template.render(adj_to_animals=adj_to_animals, animal_image_map=animal_image_map)
