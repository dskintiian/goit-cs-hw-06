from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process
from pymongo import MongoClient
import urllib.parse
import mimetypes
import pathlib
import socket

WEBSERVER_PORT = 3000
SOCKET_PORT = 5000

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('front-init/index.html')
        elif pr_url.path.lstrip('/') in ['message.html', 'index.html']:
            self.send_html_file('front-init/' + pr_url.path)
        elif pathlib.Path().joinpath('front-init/' + pr_url.path).exists():
            self.send_static()
        else:
            self.send_html_file('front-init/error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'./front-init/{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.send_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_to_socket(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = '', SOCKET_PORT
        sock.sendto(data, server)
        sock.close()

def run_webserver(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', WEBSERVER_PORT)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def run_socketserver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = '', SOCKET_PORT
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024*1024)
            save_bdata_to_mongo(data)

    except KeyboardInterrupt:
        sock.close()

def save_bdata_to_mongo(data):
    data_dict = {key: urllib.parse.unquote_plus(value) for key, value in [el.split('=') for el in data.decode('utf-8').split('&')]}
    client = MongoClient('mongodb://mongodbuser:mongodbpswd@database:27017')
    db = client['goit']
    db['messages'].insert_one({**data_dict, 'date': datetime.now()})

def main():
    process_web_server = Process(target=run_webserver)
    process_web_server.start()
    process_socket_server = Process(target=run_socketserver)
    process_socket_server.start()

if __name__ == "__main__":
    main()
