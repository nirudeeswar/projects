import cv2
import numpy as np

# Load the image in grayscale
image_path = "/Users/nirudeeswar/Desktop/vein.png"  # Update to your image path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Check if the image was loaded correctly
if image is None:
    print(f"Error: Unable to load the image from {image_path}. Check the file path.")
    exit()

# Crop the region of interest (y: 300 to 100, x: 0 to 400)
cropped_image = image[100:300, 0:400]

# Convert to binary (0 and 1) using thresholding
_, binary_image = cv2.threshold(cropped_image, 128, 1, cv2.THRESH_BINARY)

# Save the binary data to a text file
output_file_path = "/Users/nirudeeswar/Desktop/vein_binary_data.txt"  # Update as needed
np.savetxt(output_file_path, binary_image, fmt='%d')

print(f"Binary data saved to {output_file_path}")
