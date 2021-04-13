import json
import pytest

from get_mock_data import get_campsites, get_facilities

def test_get_facilities():
    file_name = get_facilities("OR")
    with open(file_name) as f:
        res = json.load(f)
    assert res.get('RECDATA') is not None

def test_get_campsites():
    facility_id = 251434
    file_name = get_campsites(facility_id)
    with open(file_name) as f:
        res = json.load(f)
    assert res.get('RECDATA') is not None