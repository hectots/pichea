#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import os


class MockRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def processRequest(self, method):
        if self.save_request:
            request_file_name = f'{method}.request.txt'
            request_file_full_path = os.path.join(
                self.mock_path,
                self.path[1:],
                request_file_name)

            with open(request_file_full_path, 'wb') as request_file:
                request_file.write(self.rfile.read(
                    int(self.headers["Content-Length"])))

        filename = f'{method}.json'
        fullpath = os.path.join(
            self.mock_path,
            self.path[1:],
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "pichea", description="Maps HTTP requests to JSON files.")
    parser.add_argument("--save-request", "-s",
                        action='store_true', help="Saves requests to a file.")
    parser.add_argument(
        "--port", "-p", help="Server's port number.", type=int, default=8282)
    parser.add_argument(
        "mock_path", help="Base path to JSON files. Default is the current directory.", nargs='?', default=os.getcwd())

    args = parser.parse_args()

    s = ThreadingHTTPServer(('localhost', args.port), type("MockRequestHandlerAug", (MockRequestHandler,), dict(
        mock_path=args.mock_path, save_request=args.save_request)))
    s.serve_forever()
    s.server_close()
