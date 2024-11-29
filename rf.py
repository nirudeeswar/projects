import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Specify the image path
image_path = "/Users/nirudeeswar/Desktop/output.png"

# Check if the file exists
if not os.path.exists(image_path):
    print(f"Image file does not exist at the specified path: {image_path}")
else:
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Failed to load the image. The file might not be a valid image.")
    else:
        print("Image loaded successfully!")

        # Perform edge detection using Robert, Sobel, and Prewitt filters

        # 1. Robert's Filter
        robert_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
        robert_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        robert_x_edges = cv2.filter2D(image, -1, robert_x)
        robert_y_edges = cv2.filter2D(image, -1, robert_y)
        robert_edges = cv2.magnitude(robert_x_edges.astype(np.float32), robert_y_edges.astype(np.float32))

        # 2. Sobel Filter
        sobel_x_edges = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y_edges = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        sobel_edges = cv2.magnitude(sobel_x_edges, sobel_y_edges)

        # 3. Prewitt Filter
        prewitt_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        prewitt_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
        prewitt_x_edges = cv2.filter2D(image, -1, prewitt_x)
        prewitt_y_edges = cv2.filter2D(image, -1, prewitt_y)
        prewitt_edges = cv2.magnitude(prewitt_x_edges.astype(np.float32), prewitt_y_edges.astype(np.float32))

        # Convert edge magnitudes to displayable format
        robert_edges = np.uint8(np.clip(robert_edges, 0, 255))
        sobel_edges = np.uint8(np.clip(sobel_edges, 0, 255))
        prewitt_edges = np.uint8(np.clip(prewitt_edges, 0, 255))

        # Plot the results
        plt.figure(figsize=(20, 10))

        # Original image
        plt.subplot(2, 2, 1)
        plt.title("Original Image")
        plt.imshow(image, cmap="gray")
        plt.axis("off")

        # Robert's Filter
        plt.subplot(2, 2, 2)
        plt.title("Robert's Edge Detection")
        plt.imshow(robert_edges, cmap="gray")
        plt.axis("off")

        # Sobel Filter
        plt.subplot(2, 2, 3)
        plt.title("Sobel Edge Detection")
        plt.imshow(sobel_edges, cmap="gray")
        plt.axis("off")

        # Prewitt Filter
        plt.subplot(2, 2, 4)
        plt.title("Prewitt Edge Detection")
        plt.imshow(prewitt_edges, cmap="gray")
        plt.axis("off")

        # Show the plots
        plt.tight_layout()
        plt.show()
