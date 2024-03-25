import socket

# Define host and port
HOST = '127.0.0.1'  # localhost
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print("Connected to the server.")

    # Function to send data to the server and receive response
    def send_data(data):
        client_socket.send(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        return response

    # Main loop for user interaction
    while True:
        try:
            print("1. Login")
            print("2. Create Account")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                response = send_data(f"login {username} {password}")
                print(response)
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                response = send_data(f"create_account {username} {password}")
                print(response)
            elif choice == "3":
                send_data("exit")
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    client_socket.close()
