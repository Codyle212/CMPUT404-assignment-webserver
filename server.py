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
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)
        decoded_data = self.data.decode('utf-8')
        request_array = decoded_data.split()
        print(request_array)
        # only need method and path
        request_method = request_array[0]
        request_route = request_array[1]
        if request_method != 'GET':
            # 405 if not GET
            http_405 = f'HTTP/1.1 405 Method Not Allowed'
            self.request.sendall(http_405.encode('utf-8'))
        else:
            # 3 ways of handling 1.correct path,2correct path missing /,3 incorrect path
            path = os.path.join(os.getcwd()+"/www"+request_route)
            if os.path.isfile(path):
                file_extension = os.path.splitext(file_path)[1]
        path = os.path.join(os.getcwd()+"/www"+request_route)

        self.request.sendall(bytearray("OK", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
