import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Response:
    def __init__(self, status_code=200, reason='OK', text=""):
        self.status_code = status_code
        self.reason = reason
        self.text = text

    def __repr__(self):
        return str({"status_code": self.status_code, "reason": self.reason, "text": self.text})


class RequestMockError(Exception):
    pass

class RequestsMock:
    file_dir = os.path.dirname(__file__)
    relative_to_root = "../../.."
    ridb_facilities_path = f"{file_dir}/{relative_to_root}/data/RIDB/facilities"
    ridb_campsites_path = f"{file_dir}/{relative_to_root}/data/RIDB/campsites"

    @classmethod
    def do_request(cls, file):
        logger.debug(f"requesting file: {file}")
        try:
            with open(file) as f:
                return Response(text=f.read())
        except FileNotFoundError:
            return Response(500, "Not found", f"No mock data. file_name: {file}")

    @classmethod
    def get(cls, url, params={}, headers={}):
        if params.get("latitude") is not None:
            file = f"{cls.ridb_facilities_path}/{params['latitude']}_{params['longitude']}_{params['radius']}.json"
        elif url.endswith("facilities"):
            file = f"{cls.ridb_facilities_path}/{params['state']}.json"
        elif url.endswith("campsites"):
            site_id = url.split("/")[-2]
            file = f"{cls.ridb_campsites_path}/{site_id}.json"
        else:
            return Response(500, "Not found", f"No mock data for {url}, params: {params}")

        return cls.do_request(file)