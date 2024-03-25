import socket
import threading

clients = {}
accounts = {
    "client_1": 1000,
    "client_2": 1500,
    "client_3": 800
}

def handle_client(client_socket, address):
    client_id = f"client_{address[1]}"
    clients[client_id] = client_socket
    print(f"Connection from {address} with ID: {client_id}")

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        if data.startswith("TRANSFER"):
            _, recipient, amount = data.split()
            transfer_money(client_id, recipient, int(amount))
        elif data == "BALANCE":
            check_balance(client_id)

def transfer_money(sender, recipient, amount):
    if sender in accounts and recipient in accounts:
        if accounts[sender] >= amount:
            accounts[sender] -= amount
            accounts[recipient] += amount
            send_message_to_client(sender, f"Transfer of {amount} to {recipient} successful.")
        else:
            send_message_to_client(sender, "Insufficient funds for transfer.")
    else:
        send_message_to_client(sender, "Invalid account details for transfer.")

def check_balance(client_id):
    if client_id in accounts:
        balance = accounts[client_id]
        send_message_to_client(client_id, f"Your current balance is: {balance}")

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

accept_clients()
