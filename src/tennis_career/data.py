"""Retrieve and clean a player's career matches from Tennis Abstract."""

import json
import re
import pandas as pd
import requests


CAREER_URL = "https://www.tennisabstract.com/jsmatches/{}Career.js"
PLAYER_URL = "https://www.tennisabstract.com/cgi-bin/player.cgi?p={}"


def _parse_matches(js_text):
    """Extract the list of match records from a Tennis Abstract career JS file."""
    found = re.search(r"morematchmx\s*=\s*(\[\[.*?\]\])", js_text, re.DOTALL)
    if found is None:
        raise ValueError("No match data (morematchmx) found in the JS text.")
    return json.loads(found.group(1))

def _format_name(player_name):
    """Convert 'serena williams' or 'Serena Williams' to 'SerenaWilliams'."""
    words = player_name.split()
    return "".join(word[0].upper() + word[1:] for word in words)

def _extract_dob(page_text):
    """Extract the player's date of birth from a Tennis Abstract player page."""
    found = re.search(r"var\s+dob\s*=\s*(\d{8})", page_text)
    if found is None:
        raise ValueError("No date of birth found on the player page.")
    return pd.to_datetime(found.group(1), format="%Y%m%d")

def _fetch_text(url, player_name):
    """Download a Tennis Abstract page, raising a clear error if the player is missing."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    if response.status_code == 404:
        raise ValueError(
            f"Player '{player_name}' not found on Tennis Abstract. "
            "Check the spelling, e.g. 'Serena Williams'."
        )
    response.raise_for_status()
    return response.text