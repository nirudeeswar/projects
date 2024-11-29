from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_file(file_path, key, output_path):
    """
    Encrypts the contents of a file using DES.
    :param file_path: Path to the file to be encrypted.
    :param key: 8-byte key for DES encryption.
    :param output_path: Path to save the encrypted file.
    """
    if len(key) != 8:
        raise ValueError("Key must be exactly 8 bytes for DES.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a DES cipher
    cipher = DES.new(key, DES.MODE_CBC)
    iv = cipher.iv  # Initialization vector

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Pad the data and encrypt
    padded_data = pad(file_data, DES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    # Write the IV + encrypted data to the output file
    with open(output_path, "wb") as f:
        f.write(iv + encrypted_data)

    print(f"File encrypted successfully. Encrypted file saved as: {output_path}")


def decrypt_file(encrypted_file_path, key, output_path):
    """
    Decrypts the contents of an encrypted file using DES.
    :param encrypted_file_path: Path to the encrypted file.
    :param key: 8-byte key for DES decryption.
    :param output_path: Path to save the decrypted file.
    """
    if len(key) != 8:
        raise ValueError("Key must be exactly 8 bytes for DES.")

    if not os.path.exists(encrypted_file_path):
        raise FileNotFoundError(f"File not found: {encrypted_file_path}")

    with open(encrypted_file_path, "rb") as f:
        encrypted_data = f.read()

    # Split the IV and the encrypted data
    iv = encrypted_data[:DES.block_size]
    encrypted_data = encrypted_data[DES.block_size:]

    # Create a DES cipher for decryption
    cipher = DES.new(key, DES.MODE_CBC, iv)

    # Decrypt and unpad the data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    print(f"File decrypted successfully. Decrypted file saved as: {output_path}")


# Main function
if __name__ == "__main__":
    # Specify paths to the input, encrypted, and decrypted files
    input_file = "image_binary.txt"  # Change to the full path if necessary
    encrypted_file = "image_binary_encrypted.txt"  # Output file for encrypted data
    decrypted_file = "image_binary_decrypted.txt"  # Output file for decrypted data

    # Example 8-byte DES key (must be exactly 8 bytes)
    des_key = b"my8key!!"

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found. Creating a test file.")
        with open(input_file, "w") as f:
            f.write("This is a test file for DES encryption.")

    # Encrypt the file
    try:
        encrypt_file(input_file, des_key, encrypted_file)
    except Exception as e:
        print(f"Error during encryption: {e}")

    # Decrypt the file
    try:
        decrypt_file(encrypted_file, des_key, decrypted_file)
    except Exception as e:
        print(f"Error during decryption: {e}")
