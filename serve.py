#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 54385
BIND = "127.0.0.1"
BASE = "/lectures"

# Define a custom handler that rewrites requests
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if the request path starts with "/lectures"
        if self.path.startswith(BASE):
            # Remove "/lectures" from the path to serve from the correct directory
            self.path = self.path.removeprefix(BASE)
            super().do_GET()
        else:
            # Send a 404 response if the path does not start with "/lectures"
            self.send_error(404, "File not found")


    # def translate_path(self, path):
    #     # Prepend '/lectures' to all paths
    #     path_a = path
    #     path_b = path.removeprefix(BASE)
    #     path_c = super().translate_path(path_b)
    #     print(f"{path_a} -> {path_b} -> {path_c}")
    #     return path_c

# Set the working directory for the server (where your slides folder is located)
os.chdir(".")

# Create the server object
with socketserver.TCPServer((BIND, PORT), MyHttpRequestHandler) as httpd:
    print(f"Serving on http://{BIND}:{PORT}{BASE}/")
    httpd.serve_forever()
