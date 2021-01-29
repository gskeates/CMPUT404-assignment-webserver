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

    def handle(self):
        # Receive data from client
        self.data = self.request.recv(1024).strip()
        # print(self.data)
        # Check for empty response
        if len(self.data) == 0:
            self.request.sendall(bytearray('HTTP/1.1 400 Bad Request\r\nConnection: close', 'utf-8'))
            return

        # Parse request for type of request and relative path to file
        method = self.data.split()[0].decode('utf-8')

        if method == 'GET':
            # Parse data
            file_name = self.data.split()[1].decode('utf-8')
            path_to_file = './www' + file_name
            # Check if path exists
            file_exists = os.path.exists('./www/' + os.path.abspath(file_name))

            if file_exists:
                # For 301 handling
                redirect = False

                # Serve index.html if given a directory
                if os.path.isdir(path_to_file):
                    if path_to_file[-1] == '/':
                        path_to_file += 'index.html'
                    else:
                        path_to_file += '/index.html'
                        redirect = True

                # Open and read data from file
                file = open(path_to_file, "r")
                file_contents = file.read()
                file.close()

                # Send file contents to client
                if not redirect:
                    content_type = path_to_file.split('.')[-1].strip()
                    server_response = 'HTTP/1.1 200 OK\r\nContent-Type: text/{}\r\n\r\n{}'.format(content_type, file_contents)
                # Redirect and send file contents
                else:
                    server_response = 'HTTP/1.1 301 Moved Permanently\r\nLocation: {}/\r\n\r\n'.format(file_name)

            # File doesn't exist
            else:
                server_response = 'HTTP/1.1 404 Not Found\r\n'

        # Only serving GET requests
        else:
            server_response = 'HTTP/1.1 405 Method Not Allowed\r\n'
        self.request.sendall(bytearray(server_response, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
