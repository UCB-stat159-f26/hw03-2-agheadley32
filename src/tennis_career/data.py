"""Retrieve and clean a player's career matches from Tennis Abstract."""

import json
import re


def _parse_matches(js_text):
    """Extract the list of match records from a Tennis Abstract career JS file."""
    found = re.search(r"morematchmx\s*=\s*(\[\[.*?\]\])", js_text, re.DOTALL)
    if found is None:
        raise ValueError("No match data (morematchmx) found in the JS text.")
    return json.loads(found.group(1))