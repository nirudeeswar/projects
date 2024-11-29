from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# File paths
input_file = "/Users/nirudeeswar/Desktop/vein_binary_data_encrypted.txt"  # Update this path
output_file = "/Users/nirudeeswar/Desktop/vein_binary_data_encrypted_aes.txt"

# AES key (16, 24, or 32 bytes). Ensure it's the correct length.
key = b'mysecurekey12345'  # 16 bytes key
iv = b'initialvector123'  # 16 bytes IV (Initialization Vector)

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: File not found at {input_file}. Please check the path.")
    exit()

# Read the input file
with open(input_file, 'rb') as f:
    data = f.read()

# Encrypt the data
cipher = AES.new(key, AES.MODE_CBC, iv)
padded_data = pad(data, AES.block_size)  # Pad data to match AES block size (16 bytes)
encrypted_data = cipher.encrypt(padded_data)

# Write the encrypted data to the output file
with open(output_file, 'wb') as f:
    f.write(encrypted_data)

print(f"File encrypted successfully using AES. Saved to {output_file}")
