"""
Image Processing Workload - Perfect for DCP Distribution
=========================================================
This workload performs computationally intensive image processing operations.
Each image or filter operation is independent, making it ideal for distributed computing.

Computational Characteristics:
- CPU-intensive: Nested loops over pixels and kernels
- Embarrassingly parallel: Each image/filter can be processed independently
- Memory-intensive: Large arrays for image data
- Real-world application: Computer vision, medical imaging, satellite imagery
"""

import numpy as np


def apply_gaussian_blur(image_size, kernel_size=15, sigma=2.0):
    """
    Apply Gaussian blur filter to an image.
    
    This is computationally expensive due to:
    1. Convolution operation over entire image
    2. Nested loops for kernel application
    3. Large kernel sizes increase computation
    
    Args:
        image_size: Size of the square image (e.g., 1000 for 1000x1000)
        kernel_size: Size of the Gaussian kernel
        sigma: Standard deviation of Gaussian distribution
    
    Returns:
        np.ndarray: Blurred image
    """
    # Generate synthetic image (in real use, this would be actual image data)
    image = np.random.rand(image_size, image_size) * 255
    
    # Create Gaussian kernel
    kernel = np.zeros((kernel_size, kernel_size))
    center = kernel_size // 2
    
    for i in range(kernel_size):
        for j in range(kernel_size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # Normalize kernel
    kernel = kernel / np.sum(kernel)
    
    # Apply convolution (computationally expensive)
    blurred = np.zeros_like(image)
    pad = kernel_size // 2
    
    for i in range(pad, image_size - pad):
        for j in range(pad, image_size - pad):
            # Extract region
            region = image[i-pad:i+pad+1, j-pad:j+pad+1]
            # Apply kernel
            blurred[i, j] = np.sum(region * kernel)
    
    return blurred


def detect_edges_sobel(image_size):
    """
    Detect edges in an image using Sobel operator.
    
    Edge detection requires computing gradients in both x and y directions,
    making it computationally intensive for large images.
    
    Args:
        image_size: Size of the square image
    
    Returns:
        dict: Contains edge magnitude and direction
    """
    # Generate synthetic image
    image = np.random.rand(image_size, image_size) * 255
    
    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
    
    # Initialize gradient arrays
    gradient_x = np.zeros_like(image)
    gradient_y = np.zeros_like(image)
    
    # Apply Sobel operators
    for i in range(1, image_size - 1):
        for j in range(1, image_size - 1):
            region = image[i-1:i+2, j-1:j+2]
            gradient_x[i, j] = np.sum(region * sobel_x)
            gradient_y[i, j] = np.sum(region * sobel_y)
    
    # Compute edge magnitude and direction
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    direction = np.arctan2(gradient_y, gradient_x)
    
    return {
        'magnitude': magnitude,
        'direction': direction,
        'max_magnitude': np.max(magnitude),
        'mean_magnitude': np.mean(magnitude)
    }


def compute_histogram_equalization(image_size, num_bins=256):
    """
    Perform histogram equalization to enhance image contrast.
    
    This involves computing histograms and cumulative distribution functions,
    which requires multiple passes over the image data.
    
    Args:
        image_size: Size of the square image
        num_bins: Number of histogram bins
    
    Returns:
        np.ndarray: Equalized image
    """
    # Generate synthetic grayscale image
    image = (np.random.rand(image_size, image_size) * 255).astype(np.uint8)
    
    # Compute histogram
    histogram = np.zeros(num_bins)
    for i in range(image_size):
        for j in range(image_size):
            histogram[image[i, j]] += 1
    
    # Compute cumulative distribution function
    cdf = np.zeros(num_bins)
    cdf[0] = histogram[0]
    for i in range(1, num_bins):
        cdf[i] = cdf[i-1] + histogram[i]
    
    # Normalize CDF
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    cdf_normalized = cdf_normalized.astype(np.uint8)
    
    # Apply equalization
    equalized = np.zeros_like(image)
    for i in range(image_size):
        for j in range(image_size):
            equalized[i, j] = cdf_normalized[image[i, j]]
    
    return equalized


def apply_morphological_operations(image_size, operation='erosion', iterations=5):
    """
    Apply morphological operations (erosion, dilation) to binary images.
    
    Multiple iterations of morphological operations are computationally expensive,
    especially for large images and large structuring elements.
    
    Args:
        image_size: Size of the square image
        operation: 'erosion' or 'dilation'
        iterations: Number of times to apply the operation
    
    Returns:
        np.ndarray: Processed binary image
    """
    # Generate synthetic binary image
    image = (np.random.rand(image_size, image_size) > 0.5).astype(np.uint8)
    
    # 3x3 structuring element
    structuring_element = np.array([[0, 1, 0],
                                     [1, 1, 1],
                                     [0, 1, 0]])
    
    result = image.copy()
    
    for iteration in range(iterations):
        temp = np.zeros_like(result)
        
        for i in range(1, image_size - 1):
            for j in range(1, image_size - 1):
                region = result[i-1:i+2, j-1:j+2]
                
                if operation == 'erosion':
                    # Erosion: minimum of region where structuring element is 1
                    temp[i, j] = np.min(region[structuring_element == 1])
                else:  # dilation
                    # Dilation: maximum of region where structuring element is 1
                    temp[i, j] = np.max(region[structuring_element == 1])
        
        result = temp
    
    return result


def compute_fourier_features(image_size):
    """
    Compute Fourier transform features for frequency analysis.
    
    FFT computation is O(n log n) but still computationally intensive
    for large images, especially when computing power spectrum and phase.
    
    Args:
        image_size: Size of the square image
    
    Returns:
        dict: Contains power spectrum and dominant frequencies
    """
    # Generate synthetic image
    image = np.random.rand(image_size, image_size) * 255
    
    # Compute 2D FFT (this is the expensive operation)
    fft = np.fft.fft2(image)
    fft_shifted = np.fft.fftshift(fft)
    
    # Compute power spectrum
    power_spectrum = np.abs(fft_shifted) ** 2
    
    # Compute phase
    phase = np.angle(fft_shifted)
    
    # Find dominant frequencies
    magnitude = np.abs(fft_shifted)
    center = image_size // 2
    
    # Compute radial frequency distribution
    radial_profile = np.zeros(center)
    for i in range(image_size):
        for j in range(image_size):
            radius = int(np.sqrt((i - center)**2 + (j - center)**2))
            if radius < center:
                radial_profile[radius] += magnitude[i, j]
    
    return {
        'power_spectrum_mean': np.mean(power_spectrum),
        'power_spectrum_max': np.max(power_spectrum),
        'dominant_frequency': np.argmax(radial_profile),
        'radial_profile': radial_profile
    }


# Example usage - this would be the input for dcpify
if __name__ == "__main__":
    # Process multiple images with different parameters
    image_sizes = [500, 1000, 1500, 2000]
    
    print("Applying Gaussian Blur...")
    for size in image_sizes:
        result = apply_gaussian_blur(size, kernel_size=15)
        print(f"Image size {size}x{size}: Blur applied, mean value = {np.mean(result):.2f}")
    
    print("\nDetecting Edges...")
    for size in image_sizes:
        result = detect_edges_sobel(size)
        print(f"Image size {size}x{size}: Max edge magnitude = {result['max_magnitude']:.2f}")
    
    print("\nComputing Fourier Features...")
    for size in image_sizes:
        result = compute_fourier_features(size)
        print(f"Image size {size}x{size}: Dominant frequency = {result['dominant_frequency']}")
