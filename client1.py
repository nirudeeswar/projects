import socket
import json
import math

def calculate_angle(p1, p2):
    """Calculate the angle between two points in degrees."""
    angle = math.atan2(p2["y"] - p1["y"], p2["x"] - p1["x"]) * 180 / math.pi
    return angle

def get_user_input():
    """
    Collect user inputs and return them as a dictionary.
    """
    dna_pattern = input("Enter DNA pattern: ")
    vein_pattern_hex = input("Enter vein pattern (hexadecimal): ")
    oxygen_meter = int(input("Enter oxygen meter: "))

    minutiae_data = []
    num_minutiae = int(input("Enter the number of minutiae points: "))
    for i in range(num_minutiae):
        x = int(input(f"Enter x-coordinate for minutiae {i+1}: "))
        y = int(input(f"Enter y-coordinate for minutiae {i+1}: "))
        minutiae_data.append({"x": x, "y": y})

    # Calculate angles for minutiae data
    for i in range(num_minutiae - 1):
        angle = calculate_angle(minutiae_data[i], minutiae_data[i+1])
        minutiae_data[i]["angle"] = angle

    # Create a dictionary to hold all input data
    data = {
        "dna_pattern": dna_pattern,
        "vein_pattern_hex": vein_pattern_hex,
        "oxygen_meter": oxygen_meter,
        "minutiae": minutiae_data,
    }

    return data

def send_data_to_server(data, client_socket):
    """Send JSON data to the server."""
    json_data = json.dumps(data)
    client_socket.sendall(json_data.encode())

# Connect to the server
server_address = ("localhost", 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# First input: Store data on the server
print("Enter your details for storage:")
initial_data = get_user_input()
send_data_to_server(initial_data, client_socket)
response = client_socket.recv(1024).decode()
print("Server response:", response)

# Second input: Validate against stored data
print("\nEnter your details again for verification:")
new_data = get_user_input()
send_data_to_server(new_data, client_socket)
response = client_socket.recv(1024).decode()
print("Server response:", response)

# Close the socket
client_socket.close()

