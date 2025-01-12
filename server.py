#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def throw_404_error(self):
        body = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n"
        body += "<HTML><body>Error 404 Not Found</body></HTML>\n"

        return body

    def handle_get_request(self):
        """Fetches the body of the webpage to be rendered by the web client

        Returns:
            The body of the webpage to be rendered by the web client
        """

        current_path = os.path.dirname(os.path.realpath(__file__))
        requested_path = current_path + "/www" + str(self.path, "utf-8")

        requested_path_split = requested_path.split("/")

        # Referenced from: https://www.geeksforgeeks.org/python-os-path-isdir-method/
        if os.path.isdir(requested_path) and requested_path[-1] != "/":
            body = "HTTP/1.1 301 Moved Permanently\nContent-Type: text/html\n\n"
            body += "<HTML><body>301 Moved Permanently</body></HTML>\n"

            return body
        
        if " " in requested_path_split[-1]:
            requested_html_filename = requested_path + "index.html"
        elif "html" in requested_path_split[-1]:
            requested_html_filename = requested_path
        else:
            requested_html_filename = requested_path + "/index.html"

        if ".." in requested_path:
            return self.throw_404_error()


        if "css" in requested_path:
            requested_css_filename = requested_path
        else:
            requested_css_filename = requested_html_filename.replace("index.html", "deep.css") if "deep" in requested_html_filename else requested_html_filename.replace("index.html", "base.css")
        body = ""

        try:
            if "css" not in requested_path:
                html_file = open(requested_html_filename) if "css" not in requested_html_filename else False

                body = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" if html_file else "HTTP/1.1 200 OK\nContent-Type: text/css\n\n" 
                
                if html_file:
                    body += html_file.read()
                    html_file.close()
            else:
                body = "HTTP/1.1 200 OK\nContent-Type: text/css\n\n" 
                
                css_file = open(requested_path)
                body += css_file.read()

                return body

        except:
            try:
                css_file = open(requested_css_filename)
                css_file.close()
            except:
                # We can only serve files in "./www" and deeper
                body = self.throw_404_error()
        
        return body
    
    def handle_other_request(self):
        """Attempts to handle HTTP requests that aren't GET

        Returns: A 405 error code as this webserver doesn't support HTTP methods other than GET
        """
        body = "HTTP/1.1 405 Method Not Allowed\nContent-Type: text/html\n\n"
        body += "<HTML><body>405 Method Not Allowed</body></HTML>"

        return body
    
    def deprecated_handle_get_request(self):
        """Fetches the body of the webpage to be rendered by the web client

        Returns:
            The body of the webpage to be rendered by the web client
        """
        
        if self.path == b"/" or self.path ==  b"/index.html":
            html_file = open("./www/index.html")
            css_file = open("./www/base.css")
            body = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
            body += "<style>"
            body += css_file.read()
            body += "</style>"
            body += "\n"
            body += html_file.read()
            
            html_file.close()
            css_file.close()
        elif self.path == b"/base.css":
            css_file = open("./www/base.css")
            body = "HTTP/1.1 200 OK\nContent-Type: text/css\n\n"
            body += "<style>\n"
            body += css_file.read()
            body += "</style>"
            body += "\n"

            css_file.close()

        elif self.path == b"/deep/" or self.path == b"/deep/index.html":
            html_file = open("./www/deep/index.html")
            css_file = open("./www/deep/deep.css")
            body = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
            body += "<style>"
            body += css_file.read()
            body += "</style>"
            body += html_file.read()
            html_file.close()
            css_file.close()

        else:
            # We can only serve files in "./www" and deeper
            body = "HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n"
            body += "<HTML><body>Error 404 Not Found</body></HTML>"
        
        return body

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.split(b" ")

        self.http_method = self.data[0]
        self.path = self.data[1]

        if self.http_method == b"GET":            
            body = self.handle_get_request()
            self.request.sendall(bytearray(body,'utf-8'))
        else:
            body = self.handle_other_request()
            self.request.sendall(bytearray(body, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
