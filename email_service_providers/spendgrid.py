import json
import requests


class SpendgridClient:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://bw-interviews.herokuapp.com/spendgrid/'
        self.base_headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }

    def send_email(self, payload):
        headers = self.base_headers
        url = self.base_url + 'send_email'
        return requests.post(url, headers=headers, data=json.dumps(payload))
