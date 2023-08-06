import datetime
import logging
import requests

logger = logging.getLogger(__file__)

class Task:
    exposed = True

    def __init__(self, server):
        self.server = server

    def GET(self, id=None):
        return self.server.status(job_id=id)

    def POST(self, script=None, id=None, cores=None):
        return self.server.submit(script, id, cores)


class Status:
    exposed = True

    def __init__(self, host, port):
        self.default_host = host
        self.default_port = port

    @staticmethod
    def proxy_url(host, port):
        return "http://{}:{}/status".format(host, port)

    def GET(self, **kwargs):
        return requests.get(
            self.proxy_url(
                kwargs.get('host', self.default_host),
                kwargs.get('port', self.default_port)
            ), params=kwargs)

    def POST(self, **kwargs):
        return requests.post(self.proxy_url(
                kwargs.get('host', self.default_host),
                kwargs.get('port', self.default_port)
            ), data=kwargs)


class Ping:
    exposed = True

    def GET(self):
        return "{}".format(datetime.datetime.now())

    def POST(self):
        return "{}".format(datetime.datetime.now())
