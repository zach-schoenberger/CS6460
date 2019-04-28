import http.client
import socketserver
import urllib
from http.server import BaseHTTPRequestHandler
from urllib import parse
import os
import subprocess
from urllib.parse import urlparse

import requests

waitResult = None


class JhubRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200, "success")
        self.end_headers()

    def do_POST(self):
        global waitResult
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200, "success")
        self.end_headers()
        waitResult = post_data


class JhubSpawnerClient(object):
    global waitResult
    jhubUrl = "jupyter-spawner.jhub.svc.cluster.local"
    jhubPort = 80
    # jhubUrl = "localhost"
    # jhubPort = 8888

    def __init__(self, port):
        self.port = port
        self.Handler = JhubRequestHandler

    def sendNotebook(self, notebook, assignment, force=False):
        nbData = ""
        with open(notebook) as nb:
            for line in nb:
                nbData += line
        ip = subprocess.Popen("hostname -i", shell=True, stdout=subprocess.PIPE).stdout.read().strip()

        params = {'uid': self.getVar('JUPYTERHUB_USER'),
                  'adr': ip,
                  'prt': self.port,
                  'asnmt': assignment,
                  'frc': force
                  }
        query = urllib.parse.urlencode(params)
        uri = "http://%s:%d/notebook/run?%s" % (self.jhubUrl, self.jhubPort, query)
        print(uri)
        resp = requests.post(uri, data=nbData)
        return resp.text

    def waitForResult(self):
        global waitResult
        with socketserver.TCPServer(("", self.port), self.Handler) as httpd:
            try:
                print("serving at port ", self.port)
                httpd.handle_request()
            except KeyboardInterrupt:
                pass
            httpd.server_close()
        result = waitResult

        return result

    def getVar(self, name, default="NULL"):
        value = os.environ.get(name)
        if value is None:
            return default
        return value


