import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the fingerprint image
image_path = "/Users/nirudeeswar/Desktop/newimage.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded successfully
if image is None:
    raise FileNotFoundError(f"Unable to load the image from the path: {image_path}")

# Convert to binary
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Invert the image
binary_image = 255 - binary_image

# Skeletonization using OpenCV
def skeletonize(img):
    skel = np.zeros(img.shape, np.uint8)
    temp = np.zeros(img.shape, np.uint8)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    while True:
        eroded = cv2.erode(binary, None)
        temp = cv2.dilate(eroded, None)
        temp = cv2.subtract(binary, temp)
        skel = cv2.bitwise_or(skel, temp)
        binary = eroded.copy()

        if cv2.countNonZero(binary) == 0:
            break

    return skel

skeleton = skeletonize(binary_image)

# Kernel for identifying neighbors
kernel = np.array([[1, 1, 1],
                   [1, 10, 1],
                   [1, 1, 1]])

# Lists to store minutiae points
termination_points = []
bifurcation_points = []

# Process the skeletonized image
rows, cols = skeleton.shape
for i in range(1, rows - 1):
    for j in range(1, cols - 1):
        if skeleton[i, j] == 255:  # Check if the pixel is part of a ridge
            # Extract the 3x3 neighborhood
            neighborhood = skeleton[i - 1:i + 2, j - 1:j + 2]
            neighbors = np.sum(neighborhood // 255) - 1  # Count neighbors excluding center

            # Termination: exactly 1 neighbor
            if neighbors == 1:
                termination_points.append((j, i))
            # Bifurcation: 3 or more neighbors
            elif neighbors >= 3:
                bifurcation_points.append((j, i))

# Plot the results
plt.figure(figsize=(10, 10))
plt.imshow(skeleton, cmap='gray')
plt.scatter([p[0] for p in termination_points], [p[1] for p in termination_points],
            color='red', label='Termination', s=10)
plt.scatter([p[0] for p in bifurcation_points], [p[1] for p in bifurcation_points],
            color='blue', label='Bifurcation', s=10)
plt.legend()
plt.title("Termination and Bifurcation Points")
plt.show()

# Print the results
print(f"Number of Termination Points: {len(termination_points)}")
print(f"Number of Bifurcation Points: {len(bifurcation_points)}")
