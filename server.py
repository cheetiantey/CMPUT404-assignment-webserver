#  coding: utf-8 
import socketserver

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

    def handle_get_request(self):
        """Fetches the body of the webpage to be rendered by the web client

        Returns:
            The body of the webpage to be rendered by the web client
        """
        if self.path.startswith(b"/www/deep"):
            html_file = open("./www/deep/index.html")
            css_file = open("./www/deep/deep.css")
            body = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
            body += "<style>"
            body += css_file.read()
            body += "</style>"
            body += html_file.read()
            html_file.close()
            css_file.close()
            # print(body)

        elif self.path.startswith(b"/www"):
            print("TRUE**************")
            # self.request.sendall(b"""
            #     <html>
            #         <body>
            #             <h1>Hello, world!</h1>
            #         </body>
            #     </html>
            # """)
            # self.request.sendall(bytearray("OK",'utf-8'))
            # self.request.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><h1>Hello, world!</h1></body></html>')
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
            # print(body)
        else:
            # We can only serve files in "./www" and deeper
            body = "HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n"
            body += "<HTML><body>Error 404 Not Found</body></HTML>"
            print(body)
        
        return body
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.split(b" ")

        self.http_method = self.data[0]
        self.path = self.data[1]

        if self.http_method == b"GET":
            print("THIS IS A GET REQUEST")
            print()
            
            body = self.handle_get_request()
            self.request.sendall(bytearray(body,'utf-8'))
        else:
            pass

        print(self.data)
        print()
        print(self.http_method)
        print()
        print(self.path)
        print()

        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
