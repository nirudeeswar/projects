import cv2
import numpy as np

def image_to_binary_txt(image_path, output_txt_path):
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image at path '{image_path}' not found!")

    # Convert to binary using thresholding
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Invert binary image for consistency (foreground white, background black)
    binary_image = 255 - binary_image

    # Convert binary image to 0s and 1s
    binary_data = (binary_image // 255).astype(int)

    # Save binary data to a text file
    with open(output_txt_path, 'w') as file:
        for row in binary_data:
            binary_line = ''.join(map(str, row))  # Convert row to a string of 0s and 1s
            file.write(binary_line + '\n')       # Write each row into the text file

    print(f"Binary data saved to '{output_txt_path}'.")

# Correct paths
image_path = "/Users/nirudeeswar/Desktop/tfimage.png"  # Update this to the path of your image
output_txt_path = "/Users/nirudeeswar/Desktop/image_binary.txt"

# Call the function
image_to_binary_txt(image_path, output_txt_path)
