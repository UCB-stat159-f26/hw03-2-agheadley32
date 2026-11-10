from pathlib import Path

import pytest

from tennis_career.data import _parse_matches

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