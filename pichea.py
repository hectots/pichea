#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
import sys

class MockRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def processRequest(self, method):
        (base_path, _) = self.path.split("?") if "?" in self.path else (self.path, "")
        directory = os.path.dirname(base_path)
        filename = f'{method}_{os.path.basename(base_path)}.json'
        fullpath = os.path.join(
            self.mock_path,
            directory[1:], # Deletes starting '/'
            filename)

        body = ""
        if os.path.exists(fullpath):
            with open(fullpath, 'r') as mock_file:
                body = mock_file.read()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(body.encode('utf-8')))
        self.end_headers()

        self.wfile.write(body.encode('utf-8'))

    def do_GET(self):
        self.processRequest("GET")
    
    def do_POST(self):
        self.processRequest("POST")
    
    def do_PUT(self):
        self.processRequest("PUT")
    
    def do_DELETE(self):
        self.processRequest("DELETE")

s = ThreadingHTTPServer(('localhost', 8282), type("MockRequestHandlerAug", (MockRequestHandler,), dict(mock_path=sys.argv[1] if len(sys.argv[1:]) > 0 else ".")))
s.serve_forever()
s.server_close()