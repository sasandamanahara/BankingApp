import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

while True:
    message = input("Enter message to send: ")
    client_socket.sendall(message.encode())
    response = client_socket.recv(1024)
    print(f"Received from server: {response.decode()}")

client_socket.close()