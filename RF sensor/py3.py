import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

# Zhang-Suen Thinning Algorithm (fixed)
def zhang_suen_thinning(image):
    img = image.copy()
    prev = np.zeros(image.shape, np.uint8)
    
    while True:
        # Step 1: First iteration
        marker = np.zeros(img.shape, np.uint8)
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if img[i, j] == 255:  # Only consider ridge pixels (255)
                    neighbors = img[i-1:i+2, j-1:j+2].flatten()
                    # Remove the center pixel
                    neighbors = np.delete(neighbors, 4)  
                    # Count the number of white neighbors (ridge pixels)
                    ridge_neighbors = np.sum(neighbors == 255)  # Only count ridge pixels
                    # Condition: At least 2 and at most 6 neighbors
                    if ridge_neighbors >= 2 and ridge_neighbors <= 6:
                        transitions = np.sum(np.abs(np.diff(neighbors))) // 255
                        if transitions == 1:
                            marker[i, j] = 255
        
        # Apply the first iteration marker
        img = cv2.subtract(img, marker)
        
        # Step 2: Second iteration (same logic as above)
        marker = np.zeros(img.shape, np.uint8)
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if img[i, j] == 255:
                    neighbors = img[i-1:i+2, j-1:j+2].flatten()
                    neighbors = np.delete(neighbors, 4)  
                    ridge_neighbors = np.sum(neighbors == 255)
                    if ridge_neighbors >= 2 and ridge_neighbors <= 6:
                        transitions = np.sum(np.abs(np.diff(neighbors))) // 255
                        if transitions == 1:
                            marker[i, j] = 255
        
        # Apply the second iteration marker
        img = cv2.subtract(img, marker)
        
        # If no changes happened, break the loop
        if np.array_equal(img, prev):
            break
        
        prev = img.copy()
    
    return img

# Function to extract minutiae (terminations and bifurcations)
def extract_minutiae(thinned_image):
    minutiae_points = {'terminations': [], 'bifurcations': []}
    height, width = thinned_image.shape
    
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if thinned_image[y, x] == 255:
                neighborhood = thinned_image[y - 1:y + 2, x - 1:x + 2]
                ridge_neighbors = np.sum(neighborhood == 255)  # Count ridge neighbors

                if ridge_neighbors == 2:  # Termination
                    minutiae_points['terminations'].append((x, y))
                elif ridge_neighbors >= 4:  # Bifurcation
                    minutiae_points['bifurcations'].append((x, y))

    return minutiae_points

# Function to check if image exists
def load_image(image_path):
    if not os.path.exists(image_path):
        print(f"Image not found at: {image_path}")
        return None
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Example: Manually specify the image path or select file
image_path = '/Users/nirudeeswar/Desktop/fingerprintextraction.png'  # Adjust this path based on your image location
image = load_image(image_path)

if image is None:
    print("Failed to load the image. Please check the file path.")
else:
    print("Image loaded successfully.")

    # Step 1: Apply Gaussian Blurring
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Step 2: Sobel Edge Detection
    sobelx = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edges = cv2.magnitude(sobelx, sobely)
    sobel_edges = np.uint8(sobel_edges)

    # Step 3: Thresholding
    _, binary_image = cv2.threshold(sobel_edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step 4: Apply Zhang-Suen Thinning
    thinned_image = zhang_suen_thinning(binary_image)

    # Step 5: Extract minutiae (terminations and bifurcations)
    minutiae = extract_minutiae(thinned_image)

    # Display the results
    plt.figure(figsize=(10, 10))
    plt.imshow(thinned_image, cmap='gray')

    # Extract x and y coordinates from minutiae points for termination and bifurcation
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
