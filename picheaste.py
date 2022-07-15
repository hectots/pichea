#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import os


class MockRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def processRequest(self, method):
        self.send_response(self.error_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len("".encode('utf-8')))
        self.end_headers()
        self.wfile.write("".encode("utf-8"))

    def do_GET(self):
        self.processRequest("GET")

    def do_POST(self):
        self.processRequest("POST")

    def do_PUT(self):
        self.processRequest("PUT")

    def do_DELETE(self):
        self.processRequest("DELETE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "picheaste", description="HTTP Server that returns desired status code.")
    parser.add_argument(
        "--port", "-p", help="Server's port number.", type=int, default=8688)
    parser.add_argument(
        "error_code", help="Status code to be returned", type=int)

    args = parser.parse_args()

    s = ThreadingHTTPServer(('localhost', args.port), type("MockRequestHandlerAug", (MockRequestHandler,), dict(error_code=args.error_code)))
    s.serve_forever()
    s.server_close()
