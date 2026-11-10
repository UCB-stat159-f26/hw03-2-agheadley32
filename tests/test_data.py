from pathlib import Path

import pandas as pd
import pytest

from tennis_career.data import _extract_dob, _format_name, _parse_matches

FIXTURES = Path(__file__).parent / "fixtures"


def read_fixture(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_parse_matches_female():
    records = _parse_matches(read_fixture("FemalePlayerCareer.js"))
    assert len(records) == 3
    assert records[0][11] == "Anne Miller"
    assert records[0][16] == "19770119"


def test_parse_matches_male():
    records = _parse_matches(read_fixture("MalePlayerCareer.js"))
    assert len(records) == 3
    assert records[2][4] == "W"
    assert records[0][16] == "22.264202601"


def test_parse_matches_without_data_raises():
    with pytest.raises(ValueError, match="morematchmx"):
        _parse_matches("<html>Page not found</html>")


@pytest.mark.parametrize(
    "raw_name", ["serena williams", "Serena Williams", "SerenaWilliams"]
)
def test_format_name_accepts_all_forms(raw_name):
    assert _format_name(raw_name) == "SerenaWilliams"


def test_extract_dob_returns_date():
    page_text = "var fullname = 'Serena Williams';\nvar dob = 19810926;"
    assert _extract_dob(page_text) == pd.Timestamp("1981-09-26")


def test_extract_dob_missing_raises():
    with pytest.raises(ValueError, match="date of birth"):
        _extract_dob("<html>No player here</html>")