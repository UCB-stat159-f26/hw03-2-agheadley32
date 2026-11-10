"""Retrieve and clean a player's career matches from Tennis Abstract."""

import json
import re
import pandas as pd
import requests


CAREER_URL = "https://www.tennisabstract.com/jsmatches/{}Career.js"
PLAYER_URL = "https://www.tennisabstract.com/cgi-bin/player.cgi?p={}"
COLUMNS = {"date": 0, "result": 4, "opponent": 11, "opponent_info": 16}


def _parse_matches(js_text):
    """Extract the list of match records from a Tennis Abstract career JS file."""
    found = re.search(r"morematchmx\s*=\s*(\[\[.*?\]\s*\])", js_text, re.DOTALL)
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


def _opponent_ages(info, dates):
    """Convert column 16 to opponent ages: a DOB in women's files, an age in men's."""
    if info.str.contains(".", regex=False).any():
        return pd.to_numeric(info, errors="coerce")
    dobs = pd.to_datetime(info, format="%Y%m%d", errors="coerce")
    return (dates - dobs).dt.days / 365.25


def _build_frame(records, player_dob):
    """Turn raw match records into a data frame of ages and results for plotting."""
    df = pd.DataFrame({col: [r[i] for r in records] for col, i in COLUMNS.items()})
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df["result"] = df["result"].map({"W": "win", "L": "loss"})
    df["player_age"] = (df["date"] - player_dob).dt.days / 365.25
    df["opponent_age"] = _opponent_ages(df["opponent_info"], df["date"])
    df["age_diff"] = df["player_age"] - df["opponent_age"]
    df = df.dropna(subset=["opponent_age"]).drop(columns="opponent_info")
    return df.reset_index(drop=True)


def get_career_matches(player_name):
    """Retrieve a player's career matches from Tennis Abstract, ready for plotting.

    Accepts names like "serena williams", "Serena Williams", or "SerenaWilliams".
    Raises ValueError if the player is not found on Tennis Abstract.
    """
    name = _format_name(player_name)
    js_text = _fetch_text(CAREER_URL.format(name), player_name)
    page_text = _fetch_text(PLAYER_URL.format(name), player_name)
    df = _build_frame(_parse_matches(js_text), _extract_dob(page_text))
    df.insert(0, "player", re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name))
    return df