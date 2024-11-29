# Core libraries
import numpy as np
import pandas as pd
import random
import math

# Image processing libraries
import cv2
import imageio
from PIL import Image, ImageFilter
import skimage
from skimage.morphology import convex_hull_image, erosion, square
from skimage.feature import hessian_matrix, hessian_matrix_eigvals
from scipy.ndimage import convolve  # Updated for correct import

# Plotting and visualization libraries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Jupyter-specific (only for notebooks)
# If you're working in Jupyter, use this magic command at the top of your notebook
# %matplotlib inline
