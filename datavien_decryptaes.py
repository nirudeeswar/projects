from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

# File paths
input_file = "/Users/nirudeeswar/Desktop/vein_binary_data_encrypted_aes.txt"  # Encrypted file path
output_file = "/Users/nirudeeswar/Desktop/vein_binary_data_decrypted.txt"  # Decrypted file path

# AES key (same as encryption)
key = b'mysecurekey12345'  # 16 bytes key
iv = b'initialvector123'  # 16 bytes IV (Initialization Vector)

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: File not found at {input_file}. Please check the path.")
    exit()

# Read the encrypted file
with open(input_file, 'rb') as f:
    encrypted_data = f.read()

# Decrypt the data
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)  # Unpad after decryption

# Write the decrypted data to the output file
with open(output_file, 'wb') as f:
    f.write(decrypted_data)

print(f"File decrypted successfully. Saved to {output_file}")
