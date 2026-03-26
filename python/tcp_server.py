import socket

class SocketServer:
    def __init__(self):
        # 常规tcp监听写法
        # server_address = ('127.0.0.1', 9999)
        # socket_family = socket.AF_INET
        # socket_type = socket.SOCK_STREAM

        # unix domain sockets 监听写法
        server_address = '/tmp/uds_socket'
        socket_family = socket.AF_UNIX
        socket_type = socket.SOCK_STREAM

        # 其他代码完全一样
        self.sock = socket.socket(socket_family, socket_type)
        self.sock.bind(server_address)
        self.sock.listen(1)
        print(f"listening on '{server_address}'.")
        pass

    def wait_and_deal_client_connect(self):
        while True:
            connection, client_address = self.sock.accept()
            data = connection.recv(1024)
            print(f"recv data from client '{client_address}': {data.decode()}")
            connection.sendall("hello client".encode())

    def __del__(self):
        self.sock.close()

if __name__ == "__main__":
    socket_server_obj = SocketServer()
    socket_server_obj.wait_and_deal_client_connect()