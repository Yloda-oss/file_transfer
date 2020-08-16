import concurrent.futures
import socket

from low_level.protocol import Protocol as Proto


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.protocol = Proto(self._server_start()[0])

    def _server_start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        #print('server ready')
        sock.listen(1)
        conn, addr = sock.accept()
        print('connection: ', addr)
        self.connection = conn, addr
        return self.connection

    def receive(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.protocol.recv_msg)
            return_value = future.result()
            return return_value


    def send(self, msg):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.protocol.send_msg, msg)
            executor.shutdown()

    def get_connection(self):
        return self.connection


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.protocol = Proto(self._server_connect())

    def _server_connect(self):
        client_sock = socket.socket()
        client_sock.connect((self.host, self.port))
        self.connection = client_sock
        return self.connection

    def receive(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.protocol.recv_msg)
            return_value = future.result()
            return return_value

    def send(self, msg):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.protocol.send_msg, msg)
            executor.shutdown()

    def get_connection(self):
        return self.connection
