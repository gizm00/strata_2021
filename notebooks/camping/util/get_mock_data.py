from bs4 import BeautifulSoup
from copy import deepcopy
from csv import DictReader
import json
import logging
import os
import requests

logger = logging.getLogger(__name__)
logger = logger.setLevel(logging.INFO)

file_dir = os.path.dirname(__file__)
relative_to_root = "../../.."
mock_data_path = f"{file_dir}/{relative_to_root}"
state_file_template = mock_data_path + "/data/RIDB/facilities/{state}.json"
campsite_file_template = mock_data_path + "/data/RIDB/campsites/{facility_id}.json"
ridb_facilities_url = "https://ridb.recreation.gov/api/v1/facilities"
campsite_details_url = ridb_facilities_url + "/{facility_id}/campsites"
params = {"activity_id":9, "state":"OR"}
headers = {"accept": "application/json", "apikey": "b2b7cf12-0a8a-413b-aa75-3125b41977b8"}

def get_facilities_near(params):
    """
    Expects latitude, longitude, radius to be set
    """
    file_name = f"{mock_data_path}/RIDB/facilities/{params['latitude']}_{params['longitude']}_{params['radius']}.json"
    response = requests.get(ridb_facilities_url, params, headers=headers)
    if response.status_code == 200:
        with open(file_name, "w+") as f:
            f.write(response.text)
    else:
        logging.error(f"Unable to get result for state {state}, got {response.reason}")
    
    return file_name

def get_facilities(state):
    file_name = f"{state_file_template.format(state = state)}"
    params["state"] = state 
    response = requests.get(ridb_facilities_url, params, headers=headers)
    if response.status_code == 200:
        with open(file_name, "w+") as f:
            f.write(response.text)
    else:
        logging.error(f"Unable to get result for state {state}, got {response.reason}")
    
    # For course limit to first page of data
    # while response['METADATA']['CURRENT_COUNT'] < response['METADATA']['TOTAL_COUNT']:
    #     params["offset"] = ['METADATA']['CURRENT_COUNT']
    #     response = requests.get(ridb_facilities_url, params, headers=headers)
    #     if response.status_code == 200:
    #         with open(f"{state_file_template.format(state = state)}", "a") as f:
    #             json.dump(response.text, f)
    #     else:
    #         break
    
    return file_name


def get_campsites(facility_id):
    file_name = f"{campsite_file_template.format(facility_id = facility_id)}"
    response = requests.get(campsite_details_url.format(facility_id = facility_id), headers=headers)
    if response.status_code == 200:
        with open(file_name, "w+") as f:
            f.write(response.text)
    else:
        logging.error(f"Unable to get result for facility_id {facility_id}, got {response.reason}")

    return file_name

def get_facilities_for(states):
    results = []
    for state in states:
        results.append(get_facilities(state))
    return results

def get_campsites_for(facilities):
    for facility_id in facilities:
        get_campsites(facility_id)

def get_nf_pages(pages):
    """
    pages: dict of {site_name: URL}
    Fetch URL and write source to file site_name.html
    """
    for page in pages:
        print(page)
        file_name = page['site_name'].replace("/", "-")
        file_path = f"../../data/NF_sites/{file_name}.html"
        res = requests.get(page['site_url'])
        if res.status_code != 200:
            logger.error(f"Unable to get page {page['site_url']}. Response: {res.reason}")
            continue
        with open(file_path, 'w+') as f:
            f.write(res.text)

def get_nf_sites(path):
    nf_sites = []
    with open(path) as f:
        reader = DictReader(f)
        for row in reader:
            nf_sites.append(row)
    
    get_nf_pages(nf_sites)


if __name__ == '__main__':
    # get_nf_sites(f"../../data/or_nf_campgrounds.csv")
    # get_facilities_near(params = {"activity_id":9, "latitude":45.4977712, "longitude":-121.8211673, "radius":15})
#     states = ['WA', 'CA']
#     state_files = get_facilities_for(states)
#     print(state_files)
#     for state_file in state_files:
#         with open(state_file) as f:
#             logging.info(f"Getting campsite data for {state_file}")
#             res = json.load(f)
#             facilities = [r['FacilityID'] for r in res['RECDATA']]
#             get_campsites_for(facilities)


