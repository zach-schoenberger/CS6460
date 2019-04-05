import http.client
import socketserver
import urllib
from http.server import BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse

import requests

global waitResult


class JhubRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.__file__)

    def do_GET(self):
        self.send_response(200, "success")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200, "success")
        self.end_headers()
        globals().waitResult = post_data


class JhubSpawnerClient(object):
    # jhubUrl = "http://jupyter-spawner.jhub.svc.cluster.local"
    jhubUrl = "localhost"

    def __init__(self, port):
        self.port = port
        self.Handler = JhubRequestHandler

    def sendNotebook(self, notebook):
        nbData = ""
        with open(notebook) as nb:
            for line in nb:
                nbData += line

        params = {'uid': 'zach',
                  'adr': self.jhubUrl,
                  'prt': self.port,
                  # 'frc': True
                  }
        query = urllib.parse.urlencode(params)
        resp = requests.post("http://%s:%d/notebook/run?%s" % (self.jhubUrl, 8888, query), data=nbData)
        return resp.text

    def waitForResult(self):
        with socketserver.TCPServer(("", self.port), self.Handler) as httpd:
            try:
                print("serving at port ", self.port)
                httpd.handle_request()
            except KeyboardInterrupt:
                pass
            httpd.server_close()
        result = globals().waitResult
        globals().waitResult = None
        return result


