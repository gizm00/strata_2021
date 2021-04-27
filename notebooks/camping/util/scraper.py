from bs4 import BeautifulSoup
import re
import requests


class Scraper:
    def __init__(self, url, facility_name):
        self.url = url
        self.facility_name = facility_name

    def get_area_status(self) :
        status = None
        try :
            for strong_tag in self.soup.find_all('strong'):
                if ('Area Status' in strong_tag.text):
                    status = strong_tag.next_sibling.strip()
        except Exception as ex:
            print('couldnt get area status %s', ex)

        return status

    # for extracting Latitude,Longitude, and Elevation
    def get_location(self, search_field):
        return_value = None
        try :
            field_div = self.soup.find_all('div', text=re.compile(search_field))
            value_div = [row.next_sibling.next_sibling for row in field_div]
            return_value  = value_div[0].text.strip()

        except Exception as ex:
            print('couldnt get location info %s', ex)

        return return_value

    # returns a dataframe of basic campground info
    def get_campground_info(self):
        info = {}
        try :
            tables = self.soup.find_all('div', {'class': 'tablecolor'})
        except Exception as ex:
            print('couldnt get tables %s', tables)
            return pd.DataFrame()

        try :
            rows = tables[0].find_all('tr')
            for row in rows:
                if row.th.text == 'Reservations:':
                    info['Reservations'] = row.td.text.strip()
                if row.th.text == 'Open Season:':
                    info['Open Season'] = row.td.text.strip()
                if row.th.text == 'Current Conditions:':
                    info['Conditions'] = row.td.text.strip()
                if row.th.text == 'Water:':
                    info['Water'] = row.td.text.strip()
                if row.th.text == 'Restroom:':
                    info['Restroom'] = row.td.text.strip()
        except Exception as ex:
            print('couldnt get basic campground info, %s', ex)
            return {}

        return info

    def get_soup(self): 
        cg_req = requests.get(self.url)
        if cg_req.status_code == 200:
            cg_soup = BeautifulSoup(cg_req.text, features="html.parser")
            return cg_soup
        return None

    # extract information from USFS webpages
    # expects row with columns url and facilityname
    # returns a df with scrape results
    def scrape(self):
        cg_info = {}
        self.soup = self.get_soup()
        cg_info['FacilityStatus'] = self.get_area_status()
        cg_info['FacilityLatitude'] = self.get_location('Latitude')
        cg_info['FacilityLongitude'] = self.get_location('Longitude')
        cg_info['FacilityElevation'] = self.get_location('Elevation')
        # Consider making this a json attribute, not separate columns
        cg_info.update(self.get_campground_info())
        cg_info['FacilityName'] = self.facility_name
        return cg_info
