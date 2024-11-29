import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Improved Minutiae Extraction Function
def extract_minutiae(thinned_image):
    minutiae_points = {'terminations': [], 'bifurcations': []}
    height, width = thinned_image.shape

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if thinned_image[y, x] == 255:  # Ridge pixel
                neighborhood = thinned_image[y - 1:y + 2, x - 1:x + 2]
                ridge_neighbors = np.sum(neighborhood == 255) - 1  # Exclude the center pixel

                if ridge_neighbors == 1:  # Termination
                    minutiae_points['terminations'].append((x, y))
                elif ridge_neighbors >= 3:  # Bifurcation
                    minutiae_points['bifurcations'].append((x, y))

    return minutiae_points

# Open file dialog to select an image
root = tk.Tk()
root.withdraw()  # Hide the root window
image_path = filedialog.askopenfilename(title="Select a fingerprint image", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])

if image_path:
    print(f"Image selected: {image_path}")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Failed to load the image.")
    else:
        print("Image loaded successfully.")

        # Step 1: Preprocessing - Gaussian Blurring
        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

        # Step 2: Adaptive Thresholding for Binarization
        binary_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 11, 2)

        # Step 3: Thinning using Zhang-Suen Algorithm
        def zhang_suen_thinning(image):
            img = image.copy()
            prev = np.zeros(img.shape, np.uint8)
            while True:
                marker = np.zeros(img.shape, np.uint8)
                for i in range(1, img.shape[0] - 1):
                    for j in range(1, img.shape[1] - 1):
                        if img[i, j] == 255:
                            neighborhood = img[i - 1:i + 2, j - 1:j + 2]
                            ridge_neighbors = np.sum(neighborhood == 255) - 1
                            if ridge_neighbors >= 2 and ridge_neighbors <= 6:
                                transitions = np.sum((neighborhood[0, 1], neighborhood[1, 2], neighborhood[2, 1], neighborhood[1, 0]) == 255)
                                if transitions == 1:
                                    marker[i, j] = 255
                img = cv2.subtract(img, marker)
                if np.array_equal(img, prev):
                    break
                prev = img.copy()
            return img

        thinned_image = zhang_suen_thinning(binary_image)

        # Step 4: Minutiae Extraction
        minutiae = extract_minutiae(thinned_image)

        # Debugging and Visualization
        plt.figure(figsize=(10, 10))
        plt.imshow(thinned_image, cmap='gray')

        # Extract x and y coordinates for terminations and bifurcations
        terminations_x, terminations_y = zip(*minutiae['terminations']) if minutiae['terminations'] else ([], [])
        bifurcations_x, bifurcations_y = zip(*minutiae['bifurcations']) if minutiae['bifurcations'] else ([], [])

        # Plot minutiae points
        plt.scatter(terminations_x, terminations_y, color='red', label='Termination', s=10)
        plt.scatter(bifurcations_x, bifurcations_y, color='blue', label='Bifurcation', s=10)

        plt.legend()
        plt.title("Minutiae Detection")
        plt.axis('off')
        plt.show()

        # Save intermediate results for debugging
        cv2.imwrite("binary_image.png", binary_image)
        cv2.imwrite("thinned_image.png", thinned_image)
        print("Intermediate results saved.")

else:
    print("No image selected.")
