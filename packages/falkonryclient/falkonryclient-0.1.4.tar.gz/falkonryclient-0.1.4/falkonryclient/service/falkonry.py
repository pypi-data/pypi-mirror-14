"""
Falkonry Client

Client to access Condition Prediction APIs

:copyright: (c) 2016 by Falkonry Inc.
:license: MIT, see LICENSE for more details.

"""

from falkonryclient.helper import schema as Schemas
from falkonryclient.service.http import HttpService

"""
FalkonryService
    Service class to link js client to Falkonry API server
"""


class FalkonryService:

    def __init__(self, host, token):
        """
        constructor
        :param host: host address of Falkonry service
        :param token: Authorization token
        """
        self.host  = host
        self.token = token
        self.http  = HttpService(host, token)

    def get_pipelines(self):
        """
        To get list of Pipelines
        """
        pipelines = []
        response  = self.http.get('/Pipeline')
        for pipeline in response:
            pipelines.append(Schemas.Pipeline(pipeline=pipeline))
        return pipelines

    def create_pipeline(self, pipeline):
        """
        To create Pipeline
        :param pipeline: Pipeline
        """
        raw_pipeline = self.http.post('/Pipeline', pipeline)
        return Schemas.Pipeline(pipeline=raw_pipeline)

    def delete_pipeline(self, pipeline):
        """
        To delete a Pipeline
        :param pipeline: string
        """
        response = self.http.delete('/Pipeline/' + str(pipeline))
        return response

    def add_input_data(self, pipeline, data):
        """
        To add data to a Pipeline
        :param pipeline: string
        :param data: json
        """
        response = self.http.fpost('/Pipeline/' + str(pipeline) + '/input', data)
        return response

    def add_input_stream(self, pipeline, data):
        """
        To add data stream to a Pipeline
        :param pipeline: string
        :param data: Stream
        """
        response = self.http.upstream('/Pipeline/' + str(pipeline) + '/input', data)
        return response

    def get_output(self, pipeline, start=None, end=None):
        """
        To get output of a Pipeline
        :param pipeline: string
        :param start: int
        :param end: int
        """
        url = '/Pipeline/' + str(pipeline) + '/output?'
        if isinstance(end, int):
            url += 'lastTime=' + str(end)
        if isinstance(start, int):
            url += '&startTime=' + str(start)
        else:
            if isinstance(start, int):
                url += '&startTime=' + str(start)
        stream = self.http.downstream(url)
        return stream
