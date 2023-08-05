"""
Falkonry Client

Client to access Condition Prediction APIs

:copyright: (c) 2016 by Falkonry Inc.
:license: MIT, see LICENSE for more details.

"""

import json
import base64
import requests
from falkonryclient.helper import utils as Utils
from cStringIO import StringIO

"""
HttpService:
    Service to make API requests to Falkonry Service
"""


class HttpService:

    def __init__(self, host, token):
        """
        constructor
        :param host: host address of Falkonry service
        :param token: Authorization token
        """
        self.host  = host if host is not None else "https://service.falkonry.io"
        self.token = base64.b64encode(token) if token is not None else ""

    def get(self, url):
        """
        To make a GET request to Falkonry API server
        :param url: string
        """

        response = requests.get(
            self.host + url,
            headers={
                'Authorization': 'Token ' + self.token
            }
        )
        if response.status_code is 200:
            return json.loads(response.content)
        else:
            raise Exception(response.content)

    def post(self, url, pipeline):
        """
        To make a POST request to Falkonry API server
        :param url: string
        :param pipeline: Pipeline
        """

        response = requests.post(
            self.host + url,
            pipeline.to_json(),
            headers={
                "Content-Type": "application/json",
                'Authorization': 'Token ' + self.token
            }
        )
        if response.status_code is 201:
            return json.loads(response.content)
        else:
            raise Exception(response.content)

    def fpost(self, url, data):
        """
        To make a form-data POST request to Falkonry API server
        :param url: string
        :param data: json
        """
        response = requests.post(
            self.host + url,
            files={
                'data': (
                    Utils.random_string(10)+'.json',
                    StringIO(json.dumps(data)),
                    'application/json;charset=UTF-8',
                    {'Expires': '0'}
                )
            },
            headers={
                'Authorization': 'Token ' + self.token
            }
        )
        if response.status_code is 202:
            return json.loads(response.content)
        else:
            raise Exception(response.content)

    def delete(self, url):
        """
        To make a DELETE request to Falkonry API server
        :param url: string
        """
        response = requests.delete(
            self.host + url,
            headers={
              'Authorization': 'Token ' + self.token
            }
        )
        if response.status_code is 200:
            return json.loads(response.content)
        else:
            raise Exception(response.content)

    def upstream(self, url, stream):
        """
        To make a form-data POST request to Falkonry API server using stream
        :param url: string
        :param stream: Stream
        """
        response = requests.post(
            self.host + url,
            files={
                'data': ('data.json', stream, 'application/json;charset=UTF-8', {'Expires': '0'})
            },
            headers={
                'Authorization': 'Token ' + self.token
            }
        )
        if response.status_code is 202:
            return json.loads(response.content)
        else:
            raise Exception(response.content)

    def downstream(self, url):
        """
        To make a GET request to Falkonry API server and return stream
        :param url: string
        """
        response = requests.get(
            self.host + url,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/x-json-stream',
                'Authorization': 'Token ' + self.token
            },
            stream=True
        )
        if response.status_code is 200:
            return response.iter_lines()
        else:
            raise Exception(response.content)
