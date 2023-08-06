import json

import httplib2

from pybagel import BagelExceptions
from pybagel import info


class Client:

    def __init__(self, product_key):
        self.http_client = httplib2.Http()
        self.product_key = product_key


    def registerDevice(self):
        headers = {
            'Product-Key': self.product_key,
            'Content-Type' : "application/json"
        }
        url = info.BAGEL_URL_BASE + "/register"
        response, content = self.http_client.request(url, 'POST', headers=headers, body=json.dumps({}))
        if int(response['status'])/100 != 2:
            raise BagelExceptions.HttpsResponseException("Error: ", response, content)
        return response['status'], content

    def sendReport(self, device_key, content):
        headers = {
            'Device-Key': device_key,
            'Content-Type' : "application/json"
        }
        url = info.BAGEL_URL_BASE + "/report"
        response, content = self.http_client.request(url, 'POST', headers=headers, body=json.dumps(content))
        if int(response['status'])/100 != 2:
            raise BagelExceptions.HttpsResponseException("Error: ", response, content)
        return response['status'], content