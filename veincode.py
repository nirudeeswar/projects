import cv2
import numpy as np
import matplotlib.pyplot as plt

# Set the correct file path to the image
image_path = "/Users/nirudeeswar/Desktop/vein.png"  # Update this path as needed
image = cv2.imread(image_path)

# Check if the image is loaded correctly
if image is None:
    print("Error: Unable to load the image. Please check the file path.")
    exit()

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Enhance contrast using CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
enhanced_image = clahe.apply(gray_image)

# Apply Gaussian Blur
blurred_image = cv2.GaussianBlur(enhanced_image, (5, 5), 0)

# Perform adaptive thresholding
thresh_image = cv2.adaptiveThreshold(
    blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3
)

# Skeletonize to get vein patterns
skeleton = np.zeros_like(thresh_image)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
temp_image = thresh_image.copy()

while True:
    eroded = cv2.erode(temp_image, element)
    temp_opened = cv2.dilate(eroded, element)
    temp_skeleton = cv2.subtract(temp_image, temp_opened)
    skeleton = cv2.bitwise_or(skeleton, temp_skeleton)
    temp_image = eroded.copy()
    if cv2.countNonZero(temp_image) == 0:
        break

# Display results
plt.figure(figsize=(10, 10))
plt.subplot(1, 4, 1), plt.title("Original"), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.subplot(1, 4, 2), plt.title("Grayscale"), plt.imshow(gray_image, cmap="gray")
plt.subplot(1, 4, 3), plt.title("Enhanced & Thresholded"), plt.imshow(thresh_image, cmap="gray")
plt.subplot(1, 4, 4), plt.title("Skeleton (Vein Pattern)"), plt.imshow(skeleton, cmap="gray")
plt.show()

