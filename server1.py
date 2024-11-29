import socket
import json

# AES encryption key (placeholder)
aes_key = b"\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10"  # Example AES key

# Global storage for user data
stored_data = None

def decrypt_aes(iv, data):
    # Placeholder for AES decryption
    return data  # Simulate returning the original data for now

def compare_data(stored, received):
    """
    Compare stored data with newly received data.
    Returns True if all fields match, else False.
    """
    return stored == received

def process_client_data(client_socket):
    global stored_data

    while True:
        # Receive data from client
        received_data = client_socket.recv(4096).decode()
        if not received_data:
            break
        
        # Parse JSON data
        data = json.loads(received_data)
        
        if stored_data is None:
            # First time: store the data
            stored_data = data
            client_socket.sendall(b"Data stored successfully. Enter inputs again for verification.")
        else:
            # Compare received data with stored data
            is_valid = compare_data(stored_data, data)
            if is_valid:
                client_socket.sendall(b"Access Granted")
            else:
                client_socket.sendall(b"Access Denied")

# Define the server address and port
server_address = ("localhost", 12345)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening...")

while True:
    # Wait for a connection
    connection, client_address = server_socket.accept()
    try:
        print(f"Connection established with {client_address}")
        process_client_data(connection)
    finally:
        connection.close()



