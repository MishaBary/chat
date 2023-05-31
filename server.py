import socket
import threading


class Clients:
    def __init__(self):
        self.clients = {}
        self.lock = threading.Lock()

    def get_client(self, name):
        with self.lock:
            return self.clients.get(name, None)

    def add_client(self, name, client_socket):
        with self.lock:
            self.clients[name] = client_socket

    def remove_client(self, name):
        with self.lock:
            if name in self.clients:
                del self.clients[name]


class DataMessage:
    def __init__(self):
        self.data_message = {}
        self.lock = threading.Lock()

    def add_message(self, receiver, message):
        with self.lock:
            if receiver in self.data_message:
                self.data_message[receiver].append(message)
            else:
                self.data_message[receiver] = [message]

    def remove_messages(self, receiver):
        with self.lock:
            if receiver in self.data_message:
                del self.data_message[receiver]


def client(client_socket, client_address):
    name_client = client_socket.recv(1024).decode()
    print(f'Connected: {name_client} ({client_address})')

    clients.add_client(name_client, client_socket)

    with data_message.lock:
        if name_client in data_message.data_message:
            for message in data_message.data_message[name_client]:
                client_socket.sendall(message.encode())
            data_message.remove_messages(name_client)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            receiver_of_letter, text = message.split(':', 1)

            recipient_socket = clients.get_client(receiver_of_letter)
            if recipient_socket:
                recipient_socket.sendall(f'{name_client}:{text}'.encode())
            else:
                data_message.add_message(
                    receiver_of_letter,
                    f'{name_client} send message: {text}\n')

        except Exception as e:
            print(f'Error: {e}')
            break

    clients.remove_client(name_client)
    client_socket.close()
    print(f'Disconnected: {name_client} ({client_address})')


def server():
    server_socket.listen(5)
    print('Server start')

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(
            target=client,
            args=(
                client_socket,
                client_address
            )
        ).start()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = 'localhost'
port = 8000
server_socket.bind((host, port))

clients = Clients()
data_message = DataMessage()

server()
