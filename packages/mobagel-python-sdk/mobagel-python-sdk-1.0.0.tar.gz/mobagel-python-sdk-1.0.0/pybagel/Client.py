import json

import httplib2

from pybagel import BagelExceptions
from pybagel import info


class Client:

    def __init__(self, product_key):
        self.http_client = httplib2.Http()
        self.product_key = product_key

    def getTime(self):
        resp, content = self.http_client.request(info.BAGEL_URL_BASE + "/time", "GET")
        if resp['status'] != "200":
            raise BagelExceptions.HttpsResponseException("get Time HTTPS response Error", resp, content)
        return content.decode('utf-8')

    def registerDevice(self):
        headers = {
            'Product-Key': self.product_key,
            'Content-Type' : "application/json"
        }
        url = info.BAGEL_URL_BASE + "/register"

        resp, content = self.http_client.request(url, 'POST', headers=headers, body=json.dumps({}))
        if resp['status'] != "200":
            raise BagelExceptions.HttpsResponseException("regist device HTTPS response Error", resp, content)
        return json.loads(content.decode('utf-8'))["data"]

    def sendReport(self, device_key, content):
        headers = {
            'Device-Key': device_key,
            'Content-Type' : "application/json"
        }
        url = info.BAGEL_URL_BASE + "/reports"
        response, content = self.http_client.request(url, 'POST', headers=headers, body=json.dumps(content))

        return content.decode('utf-8')
