import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

def send_message(message):
    client_socket.sendall(message.encode())
    response = client_socket.recv(1024).decode()
    print(response)

# Example: Transfer money from client_1 to client_2
def transfer_money(sender, recipient, amount):
    send_message(f"TRANSFER {recipient} {amount}")

transfer_money("client_1", "client_2", 200)

# Example: Check balance for client_1
send_message("BALANCE")

client_socket.close()
