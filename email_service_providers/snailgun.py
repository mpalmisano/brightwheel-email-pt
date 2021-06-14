import json
import requests


class SnailgunClient:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://bw-interviews.herokuapp.com/snailgun/'
        self.base_headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }

    def send_email(self, payload):
        headers = self.base_headers
        url = self.base_url + 'emails'
        return requests.post(url, headers=headers, data=json.dumps(payload))

    def check_email_status(self, email_id):
        headers = self.base_headers
        url = self.base_url + 'emails/' + email_id
        return requests.get(url, headers=headers)

