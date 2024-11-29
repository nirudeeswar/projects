import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image (replace this with the correct path to your image)
image_path = '/Users/nirudeeswar/Desktop/fingerprint.png'  # Update with the actual path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded correctly
if image is None:
    print(f"Failed to load the image at: {image_path}")
else:
    print(f"Image loaded successfully from: {image_path}")

    # Step 1: Gaussian Blurring to remove noise
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # ------------------------ Robert Filter ------------------------
    # Robert operator kernels for edge detection
    robert_kernel_x = np.array([[1, 0], [0, -1]], dtype=float)
    robert_kernel_y = np.array([[0, 1], [-1, 0]], dtype=float)

    # Apply Robert filter (convolve the image with the kernels)
    robert_x = cv2.filter2D(blurred_image, -1, robert_kernel_x)
    robert_y = cv2.filter2D(blurred_image, -1, robert_kernel_y)

    # Convert to float64 to avoid errors with magnitude
    robert_x = np.float64(robert_x)
    robert_y = np.float64(robert_y)

    # Compute magnitude of the gradient
    robert_edges = cv2.magnitude(robert_x, robert_y)

    # ------------------------ Sobel Filter ------------------------
    # Sobel operator kernels for edge detection
    sobel_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)  # Sobel in X direction
    sobel_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)  # Sobel in Y direction
    sobel_edges = cv2.magnitude(sobel_x, sobel_y)  # Combine X and Y edges

    # ------------------------ Prewitt Filter ----------------------
    # Prewitt operator kernels for edge detection
    prewitt_kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=float)
    prewitt_kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=float)

    # Apply Prewitt filter (convolve the image with the kernels)
    prewitt_x = cv2.filter2D(blurred_image, -1, prewitt_kernel_x)
    prewitt_y = cv2.filter2D(blurred_image, -1, prewitt_kernel_y)

    # Convert to float64 to avoid errors with magnitude
    prewitt_x = np.float64(prewitt_x)
    prewitt_y = np.float64(prewitt_y)

    # Compute magnitude of the gradient
    prewitt_edges = cv2.magnitude(prewitt_x, prewitt_y)

    # ------------------------ Display Results ---------------------
    plt.figure(figsize=(15, 10))

    # Show the original image
    plt.subplot(2, 3, 1)
    plt.title("Original Image")
    plt.imshow(image, cmap='gray')
    plt.axis('off')

    # Show the Robert edges
    plt.subplot(2, 3, 2)
    plt.title("Robert Edge Detection")
    plt.imshow(robert_edges, cmap='gray')
    plt.axis('off')

    # Show the Sobel edges
    plt.subplot(2, 3, 3)
    plt.title("Sobel Edge Detection")
    plt.imshow(sobel_edges, cmap='gray')
    plt.axis('off')

    # Show the Prewitt edges
    plt.subplot(2, 3, 4)
    plt.title("Prewitt Edge Detection")
    plt.imshow(prewitt_edges, cmap='gray')
    plt.axis('off')

    plt.show()
