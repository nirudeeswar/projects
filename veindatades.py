import os

input_file = "/Users/nirudeeswar/Desktop/vein_binary_data.txt"  # Update to the correct path
output_file = "/Users/nirudeeswar/Desktop/vein_binary_data_encrypted.txt"

if not os.path.exists(input_file):
    print(f"Error: File not found at {input_file}. Please check the path.")
    exit()

# Proceed with the encryption code
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

key = b'secure12'  # Key must be 8 bytes
with open(input_file, 'rb') as f:
    data = f.read()

cipher = DES.new(key, DES.MODE_ECB)
padded_data = pad(data, DES.block_size)
encrypted_data = cipher.encrypt(padded_data)

with open(output_file, 'wb') as f:
    f.write(encrypted_data)

print(f"File encrypted successfully. Saved to {output_file}")

