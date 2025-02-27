import pytest
from typing import List
from scraper import extract_adjectives, extract_animal

@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("cetacean or cetaceous", ["cetacean", "cetaceous"]),
        ("avian (bird-like)", ["avian"]),
        ("reptilian", ["reptilian"]),
        ("", []),  #Edge case: Empty input
    ],
)
def test_extract_adjectives(input_text: str, expected: List[str]) -> None:
    """Test extracting collateral adjectives from different formats."""
    assert extract_adjectives(input_text) == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Spider (list)", "Spider"),
        ("Alpaca [14]", "Alpaca"),
        ("Pig (list) Also see Boar", "Pig"),
        ("Elk / Wapiti", "Elk / Wapiti"),
        ("", ""),  #Edge case: Empty input
        ("   Dog   ", "Dog"),  #Edge case: Extra spaces
    ],
)
def test_extract_animal(input_text: str, expected: str) -> None:
    """
    Test extracting clean animal names from Wikipedia-style text."""
    assert extract_animal(input_text) == expected
