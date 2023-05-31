import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 8000
client_socket.connect((host, port))

guest_name = input('Enter your name: ')
client_socket.sendall(guest_name.encode())


def check_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print('\n', message)
        except Exception as e:
            print(f'Error: {e}')
            break


def send_messages():
    while True:
        try:
            receiver_of_letter = input('To whom do you want to send a message: ')
            text = input('Message: ')
            message = f'{receiver_of_letter}:{text}'
            client_socket.sendall(message.encode())
        except Exception as e:
            print(f'Error: {e}')
            break


threading.Thread(target=check_messages).start()
threading.Thread(target=send_messages).start()
