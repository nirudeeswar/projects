from Crypto.Cipher import DES, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

# Define file paths (update with your actual username)
username = "nirudeeswar"
input_file_path = f'/Users/{username}/Desktop/dnasequence.txt'
des_encrypted_file_path = f'/Users/{username}/Desktop/des_encrypted.txt'
aes_encrypted_file_path = f'/Users/{username}/Desktop/aes_encrypted.txt'

# Keys for DES and AES
des_key = get_random_bytes(8)  # DES requires an 8-byte key
aes_key = get_random_bytes(16) # AES requires a 16-byte key (128-bit)

# DES Encryption function
def des_encrypt(data, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_data = pad(data, DES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

# AES Encryption function
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

# Check if input file exists
if not os.path.exists(input_file_path):
    print(f"File not found: {input_file_path}")
else:
    # Read the DNA sequence from the input file
    with open(input_file_path, 'r') as f:
        dna_sequence = f.read().strip().encode()  # Read, strip whitespace, and encode as bytes

    # Encrypt the DNA sequence using DES
    print("Encrypting with DES...")
    des_encrypted_data = des_encrypt(dna_sequence, des_key)

    # Write DES encrypted data to a text file in hexadecimal format
    with open(des_encrypted_file_path, 'w') as f:
        f.write(des_encrypted_data.hex())
    print(f"DES Encrypted data saved at: {des_encrypted_file_path}")

    # Encrypt the DES-encrypted data using AES
    print("Encrypting DES output with AES...")
    aes_encrypted_data = aes_encrypt(des_encrypted_data, aes_key)

    # Write the AES encrypted data to a text file in hexadecimal format
    with open(aes_encrypted_file_path, 'w') as f:
        f.write(aes_encrypted_data.hex())
    print(f"AES Encrypted data saved at: {aes_encrypted_file_path}")

    # Output the encryption keys
    print(f"\nDES Key (hex): {des_key.hex()}")
    print(f"AES Key (hex): {aes_key.hex()}")

