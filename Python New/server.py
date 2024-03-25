import socket
import threading
import sqlite3
import hashlib

# Database initialization
conn = sqlite3.connect('bank.db')
c = conn.cursor()

# Create table for storing user accounts
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, balance REAL)''')
conn.commit()

# Define host and port
HOST = '127.0.0.1'  # localhost
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)  # Listen for up to 5 connections

    print("Server is listening for connections...")

    # Function to handle client connections
    def handle_client(client_socket, address):
        print(f"Connected to {address}")

        # Function to authenticate user
        def authenticate_user(username, password):
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashlib.sha256(password.encode()).hexdigest()))
            user = c.fetchone()
            if user:
                return True, user[0]  # Return user ID if authentication is successful
            else:
                return False, None

        # Function to create new user account
        def create_account(username, password):
            try:
                c.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)", (username, hashlib.sha256(password.encode()).hexdigest(), 0))
                conn.commit()
                return True, "Account created successfully."
            except sqlite3.IntegrityError:
                return False, "Username already exists."

        # Handle client requests
        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break  # If no data is received, close the connection

                # Split the received data into command and parameters
                command, *params = data.split()

                # Process client requests
                if command == "login":
                    if len(params) != 2:
                        client_socket.send("Invalid number of parameters.".encode('utf-8'))
                    else:
                        username, password = params
                        authenticated, user_id = authenticate_user(username, password)
                        if authenticated:
                            client_socket.send(f"Welcome, {username}!".encode('utf-8'))
                        else:
                            client_socket.send("Invalid username or password.".encode('utf-8'))
                elif command == "create_account":
                    if len(params) != 2:
                        client_socket.send("Invalid number of parameters.".encode('utf-8'))
                    else:
                        username, password = params
                        success, message = create_account(username, password)
                        if success:
                            client_socket.send(message.encode('utf-8'))
                        else:
                            client_socket.send(message.encode('utf-8'))
                elif command == "exit":
                    break  # Close the connection
                else:
                    client_socket.send("Invalid command.".encode('utf-8'))
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        # Close client connection
        client_socket.close()
        print(f"Connection with {address} closed.")

    # Main server loop
    while True:
        # Accept incoming connection
        client_socket, address = server_socket.accept()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the server socket
    server_socket.close()
