import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = "/mnt/data/output.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 1. Gaussian Blurring to remove noise
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

# 2. Edge Detection using Sobel
sobelx = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)
sobel_edges = cv2.magnitude(sobelx, sobely)
sobel_edges = np.uint8(sobel_edges)

# 3. Binarization using Otsu's thresholding
_, binary_image = cv2.threshold(sobel_edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 4. Morphological Transformations - Thinning
kernel = np.ones((3, 3), np.uint8)
thin_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

# 5. Display the Results
plt.figure(figsize=(20, 10))

plt.subplot(1, 4, 1)
plt.title("Original Image")
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 4, 2)
plt.title("Gaussian Blurred Image")
plt.imshow(blurred_image, cmap='gray')
plt.axis('off')

plt.subplot(1, 4, 3)
plt.title("Sobel Edge Detection")
plt.imshow(sobel_edges, cmap='gray')
plt.axis('off')

plt.subplot(1, 4, 4)
plt.title("Thinned Fingerprint Image")
plt.imshow(thin_image, cmap='gray')
plt.axis('off')

plt.show()
