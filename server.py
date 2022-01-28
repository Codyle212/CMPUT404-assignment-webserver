#  coding: utf-8
import socketserver
import mimetypes
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

    def handle(self):
        baseurl = "http://127.0.0.1:8080"
        self.data = self.request.recv(1024).strip()

        print("Got a request of: %s\n" % self.data)
        decoded_data = self.data.decode('utf-8')
        request_array = decoded_data.split()
        # only need method and path
        request_method = request_array[0]
        request_route = request_array[1]
        if request_method != 'GET':
            # 405 if not GET
            self.request.sendall(
                bytearray("HTTP/1.1 405 Method Not Allowed", 'utf-8'))

        elif '/..' in request_route or '/.' in request_route:
            # disable relative route access
            self.request.sendall(
                bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
        else:
            # 3 ways of handling 1.correct path,2correct path missing /,3 incorrect path
            path = os.path.join(os.getcwd()+"/www"+request_route)
            if os.path.isfile(path):
                if request_route.endswith('.html'):
                    # server html
                    file = open(path)
                    serving_file = file.read()
                    self.request.sendall(
                        bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{serving_file}', 'utf-8'))
                    file.close()
                elif request_route.endswith('.css'):
                    # server css
                    file = open(path)
                    serving_file = file.read()
                    self.request.sendall(
                        bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n{serving_file}', 'utf-8'))
                    file.close()
                else:
                    self.request.sendall(
                        bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
            elif os.path.isdir(path):
                # handling redirect if route doesn't end with '/'
                if not path.endswith('/'):
                    change_route = request_route + '/'
                    self.request.sendall(
                        bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + baseurl + change_route + "\r\n", 'utf-8'))
                else:
                    # serve html if user goes to the default route
                    default_route = request_route+'index.html'
                    default_path = os.path.join(
                        os.getcwd()+"/www"+default_route)
                    # server html file
                    file = open(default_path)
                    serving_file = file.read()
                    self.request.sendall(
                        bytearray(f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{serving_file}\r\n', 'utf-8'))
                    file.close()
            else:
                self.request.sendall(
                    bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
        # path = os.path.join(os.getcwd()+"/www"+request_route)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
