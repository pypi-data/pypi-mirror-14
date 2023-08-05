import httplib2
import time
import hashlib
import json

from pybagel.py3 import info
from pybagel.py3 import BagelExceptions

class Client:

    def __init__(self, device_config):
        self.http_client = httplib2.Http()
        cur_ts_a = int(time.time())
        api_ts = int(self.getTime())
        cur_ts_b = int(time.time())
        self.extra_ts = int(api_ts - (cur_ts_a+cur_ts_b)/2)
        self.product_id = device_config["product_id"]
        self.product_key = device_config["product_key"]
        self.device_id = device_config["device_id"]
        self.device_key = device_config["device_key"]


    def getTime(self):
        resp, content = self.http_client.request(info.BAGEL_URL_BASE+"/time", "GET")
        if resp['status'] != "200":
            raise BagelExceptions.HttpsResponseException("get Time HTTPS response Error", resp, content)
        return content



    def sendReport(self, content):
        report_ts = str(int(time.time())+self.extra_ts)
        to_sha256 = "{}:{}:{}:{}:{}".format(
                self.product_id, self.product_key, self.device_id, self.device_key,
                    report_ts)
        token = hashlib.sha256(to_sha256.encode('utf-8')).hexdigest()
        headers = {
            'Product-id': self.product_id,
            'Device-id' : self.device_id,
            'Token' : token,
            'Timestamp' : report_ts,
            'Content-Type' : "application/json"
        }
        url = info.BAGEL_URL_BASE + "/products/" + self.product_id + "/devices/" +self.device_id + "/reports"
        response, content = self.http_client.request(url, 'POST', headers=headers, body=json.dumps(content))


        return content


