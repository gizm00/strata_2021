import pytest

from request import requests

@pytest.mark.parametrize("state, expected", [("OR", 200), ("PA", 500)])
def test_get_facilities(state, expected):
    url = "https://ridb.recreation.gov/api/v1/facilities"
    params = {"activity_id":9, "state":state}
    headers = {"accept": "application/json", "apikey": "key"}
    resp = requests.get(url, params, headers)
    assert resp.status_code == expected

@pytest.mark.parametrize("site_id, expected", [("251434", 200), ("00000", 500)])
def test_get_campsites(site_id, expected):
    url = "https://ridb.recreation.gov/api/v1/facilities/251434/campsites"
    requests.get(url)