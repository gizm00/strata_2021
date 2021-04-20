import json
import pytest

from request import RequestsMock

@pytest.mark.parametrize("state, expected", [("OR", 200), ("PA", 500)])
def test_get_facilities(state, expected):
    url = "https://ridb.recreation.gov/api/v1/facilities"
    params = {"activity_id":9, "state":state}
    headers = {"accept": "application/json", "apikey": "key"}
    resp = RequestsMock.get(url, params, headers)
    assert resp.status_code == expected

@pytest.mark.parametrize("site_id, expected", [("251434", 200), ("00000", 500)])
def test_get_campsites(site_id, expected):
    url = f"https://ridb.recreation.gov/api/v1/facilities/{site_id}/campsites"
    response = RequestsMock.get(url)
    if response.status_code == 200:
        res = json.loads(response.text)
    assert response.status_code == expected

def test_get_near():
    ridb_facilities_url = "https://ridb.recreation.gov/api/v1/facilities"
    params = {"activity_id":9, "latitude":45.4977712, "longitude":-121.8211673, "radius":15}
    headers = {"accept": "application/json", "apikey": "key"}
    response = RequestsMock.get(ridb_facilities_url, params, headers=headers)
    assert response.status_code == 200