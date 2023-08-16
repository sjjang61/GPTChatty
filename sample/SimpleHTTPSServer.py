'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''
# http://dveamer.github.io/backend/PythonSimpleHTTPServer.html
# browser : http://localhost:4430/websocket.html
import ssl
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

if __name__ == "__main__":
    # openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
    httpd = HTTPServer(('localhost', 4430), SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='../cert.pem', keyfile='../key.pem', ssl_version=ssl.PROTOCOL_TLS)
    # httpd.socket = ssl.SSLContext.wrap_socket(httpd.socket, server_side=True, certfile='./cert.pem', keyfile='./key.pem',ssl_version=ssl.PROTOCOL_TLSv1)
    print("start https server")
    httpd.serve_forever()