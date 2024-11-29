from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import os

# Update the input file path to the correct location
input_file = "/Users/nirudeeswar/Documents/vein_binary_data_encrypted_des.txt"  # Change to the correct path
output_file = "/Users/nirudeeswar/Documents/vein_binary_data_decrypted_des.txt"  # Decrypted file output path

# Debug: Print the input file path
print(f"Trying to open file at: {input_file}")

# DES key (8 bytes). Ensure it is the correct length.
key = b'my8bytekey'  # 8-byte key for DES

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: File not found at {input_file}. Please check the path.")
    exit()

# Read the encrypted file
with open(input_file, 'rb') as f:
    encrypted_data = f.read()

# Decrypt the data using DES in ECB mode (if it was encrypted this way)
cipher = DES.new(key, DES.MODE_ECB)  # DES in ECB mode (no IV needed)
decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)  # Unpad after decryption

# Write the decrypted data to the output file
with open(output_file, 'wb') as f:
    f.write(decrypted_data)

print(f"File decrypted successfully. Saved to {output_file}")
