import json
import logging

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

class requests:
    ridb_facilities_path = "../data/RIDB/facilities"
    ridb_campsites_path = "../data/RIDB/campsites"

    @classmethod
    def do_request(cls, file):
        try:
            with open(file) as f:
                return Response(text=json.load(f))
        except FileNotFoundError:
            return Response(500, "Not found", f"No mock data")

    @classmethod
    def get(cls, url, params={}, headers={}):
        if url.endswith("facilities"):
            file = f"{cls.ridb_facilities_path}/{params['state']}.json"
        elif url.endswith("campsites"):
            site_id = url.split("/")[-2]
            file = f"{cls.ridb_campsites_path}/{site_id}.json"
        else:
            return Response(500, "Not found", f"No endpoint to service {url}")

        return cls.do_request(file)