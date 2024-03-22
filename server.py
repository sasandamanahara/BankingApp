import socket
import threading

clients = {}

def handle_client(client_socket, address):
    client_id = f"client_{address[1]}"
    clients[client_id] = client_socket
    print(f"Connection from {address} with ID: {client_id}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received from {client_id}: {data.decode()}")

def send_message_to_client(client_id, message):
    if client_id in clients:
        client_socket = clients[client_id]
        client_socket.sendall(message.encode())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9999))
server_socket.listen()

print("Server is listening for connections...")

def accept_clients():
    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

        # Example: Send a message to a specific client after connection
        send_message_to_client(f"client_{address[1]}", "Welcome to the server!")

accept_clients()