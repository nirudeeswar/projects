import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Function to check if image exists
def load_image(image_path):
    if not os.path.exists(image_path):
        print(f"Image not found at: {image_path}")
        return None
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Function to preprocess the image (Gaussian Blur, Histogram Equalization, Adaptive Thresholding)
def preprocess_image(image):
    # Gaussian Blur to reduce noise
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    # Histogram Equalization to improve contrast
    equalized_image = cv2.equalizeHist(blurred_image)
    # Adaptive Thresholding
    preprocessed_image = cv2.adaptiveThreshold(equalized_image, 255, 
                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                               cv2.THRESH_BINARY, 11, 2)
    return preprocessed_image

# Function to apply Zhang-Suen thinning
def zhang_suen_thinning(image):
    skeleton = cv2.ximgproc.thinning(image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return skeleton

# Function to extract minutiae (terminations and bifurcations)
def extract_minutiae(thinned_image):
    minutiae_points = {'terminations': [], 'bifurcations': []}
    height, width = thinned_image.shape
    
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if thinned_image[y, x] == 255:
                # Extract 3x3 neighborhood
                neighborhood = thinned_image[y - 1:y + 2, x - 1:x + 2]
                # Count the number of 255 (white pixel) neighbors
                ridge_neighbors = np.sum(neighborhood == 255)
                
                if ridge_neighbors == 2:  # Termination
                    minutiae_points['terminations'].append((x, y))
                elif ridge_neighbors >= 4:  # Bifurcation
                    minutiae_points['bifurcations'].append((x, y))
                    
    return minutiae_points

# Image path
image_path = '/Users/nirudeeswar/Desktop/fingerprintextraction.png'  # Adjust this path based on your image location

# Load the image
image = load_image(image_path)
if image is None:
    print("Failed to load the image. Please check the file path.")
else:
    print("Image loaded successfully.")

    # Step 1: Preprocess Image
    preprocessed_image = preprocess_image(image)

    # Step 2: Apply Zhang-Suen Thinning
    thinned_image = zhang_suen_thinning(preprocessed_image)

    # Step 3: Extract minutiae (terminations and bifurcations)
    minutiae = extract_minutiae(thinned_image)

    # Display the results
    plt.figure(figsize=(10, 10))
    plt.imshow(thinned_image, cmap='gray')

    # Extract x and y coordinates from minutiae points for terminations and bifurcations
    terminations_x, terminations_y = zip(*minutiae['terminations']) if minutiae['terminations'] else ([], [])
    bifurcations_x, bifurcations_y = zip(*minutiae['bifurcations']) if minutiae['bifurcations'] else ([], [])

    # Plot termination points in red and bifurcation points in blue
    plt.scatter(terminations_x, terminations_y, color='red', label='Termination', s=50)
    plt.scatter(bifurcations_x, bifurcations_y, color='blue', label='Bifurcation', s=50)

    # Add legend and title
    plt.legend()
    plt.title("Minutiae Detection")
    plt.axis('off')
    plt.show()
