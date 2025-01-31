import colorsys
import numpy as np
import argparse
from PIL import Image
import plotly.graph_objects as go

def rgb_to_wavelength(rgb_matrix):
    """
    Convert RGB values to approximate wavelengths and intensities.
    
    Args:
        rgb_matrix (np.ndarray): 3xN array of RGB values (0-255)
        
    Returns:
        np.ndarray: 2xN array where first row is wavelengths in nanometers (0 for black components)
                   and second row is intensity values (0-1).
    """
    # Convert input to float array and transpose to Nx3
    rgb = rgb_matrix.T.astype(np.float32)
    
    # Normalize RGB values
    rgb_norm = rgb / 255.0
    
    # Convert to HSV using vectorized operations
    hsv = np.apply_along_axis(lambda x: colorsys.rgb_to_hsv(*x), 1, rgb_norm)
    h, s, v = hsv.T
    
    # Initialize wavelengths array
    wavelengths = np.zeros_like(h)
    
    # Create mask for non-black pixels
    non_black_mask = v > 0
    hue_angles = h[non_black_mask] * 360
    
    # Vectorized wavelength calculations
    # Red to Yellow (0-60°)
    mask = hue_angles < 60
    wavelengths[non_black_mask] = np.where(mask, 700 - (120 * (hue_angles / 60)), wavelengths[non_black_mask])
    
    # Yellow to Green (60-120°)
    mask = (hue_angles >= 60) & (hue_angles < 120)
    wavelengths[non_black_mask] = np.where(mask, 580 - (50 * ((hue_angles - 60) / 60)), wavelengths[non_black_mask])
    
    # Green to Cyan (120-180°)
    mask = (hue_angles >= 120) & (hue_angles < 180)
    wavelengths[non_black_mask] = np.where(mask, 530 - (30 * ((hue_angles - 120) / 60)), wavelengths[non_black_mask])
    
    # Cyan to Blue (180-240°)
    mask = (hue_angles >= 180) & (hue_angles < 240)
    wavelengths[non_black_mask] = np.where(mask, 500 - (50 * ((hue_angles - 180) / 60)), wavelengths[non_black_mask])
    
    # Blue to Violet (240-300°)
    mask = (hue_angles >= 240) & (hue_angles < 300)
    wavelengths[non_black_mask] = np.where(mask, 450 - (50 * ((hue_angles - 240) / 60)), wavelengths[non_black_mask])
    
    # Magenta/Purple (300-360°)
    mask = hue_angles >= 300
    wavelengths[non_black_mask] = np.where(mask, 400 + (300 * ((hue_angles - 300) / 60)), wavelengths[non_black_mask])
    
    # Create 2xN output array with wavelengths and intensities
    result = np.vstack((wavelengths, v))
    return result

def get_wavelength_distribution(rgb_matrix, min_wavelength=380, max_wavelength=750):
    """
    Get wavelength distribution from RGB matrix with summed intensities.
    
    Args:
        rgb_matrix (np.ndarray): 3xN array of RGB values (0-255)
        min_wavelength (float): Minimum wavelength to include (nm)
        max_wavelength (float): Maximum wavelength to include (nm)
        
    Returns:
        tuple: (dict, np.ndarray) where:
            dict: {wavelength: summed_intensity} for wavelengths in range
            np.ndarray: 2D array with [wavelength, intensity] columns for all wavelengths in range
    """
    # Get wavelengths and intensities
    wavelengths, intensities = rgb_to_wavelength(rgb_matrix)
    
    # Bucket wavelengths into 5nm intervals
    bucketed_wavelengths = np.floor(wavelengths / 5) * 5
    
    # Create output dictionary
    wavelength_dist = {}
    
    # Filter and sum intensities
    for wl, intensity in zip(bucketed_wavelengths, intensities):
        if min_wavelength <= wl <= max_wavelength:
            if wl in wavelength_dist:
                wavelength_dist[wl] += intensity
            else:
                wavelength_dist[wl] = intensity
    
    # Create complete wavelength range with 10 nm steps
    all_wavelengths = np.arange(min_wavelength, max_wavelength + 1, 10)
    
    # Create 2D array with wavelengths and intensities
    wavelength_matrix = np.zeros((len(all_wavelengths), 2))
    wavelength_matrix[:, 0] = all_wavelengths
    
    # Fill in intensities from the dictionary
    for i, wl in enumerate(all_wavelengths):
        if wl in wavelength_dist:
            wavelength_matrix[i, 1] = wavelength_dist[wl]
                
    return wavelength_dist, wavelength_matrix

def _test_wavelength_conversion():
    # Simple test with basic colors
    import numpy as np
    
    # Create test colors (3x5 array: red, green, blue, magenta, black)
    test_colors = np.array([
        [125, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
        [255, 0, 255],
        [0, 0, 0]
    ]).T  # Transpose to 3xN format
    
    result = rgb_to_wavelength(test_colors)
    
    print("Color to wavelength and intensity mappings:")
    for color, (wl, intensity) in zip(test_colors.T, result.T):
        print(f"RGB{tuple(color)} -> {wl:.1f} nm, intensity {intensity:.2f}")


def _test_wavelength_distribution():
    # Create test colors with some duplicates
    test_colors = np.array([
        [125, 0, 0],  # Red
        [125, 0, 0],  # Same red
        [0, 255, 0],  # Green
        [0, 0, 255],  # Blue
        [255, 0, 255],# Magenta
        [0, 0, 0]     # Black
    ]).T  # Transpose to 3xN format
    
    distribution, wavelength_matrix = get_wavelength_distribution(test_colors)
    
    print("\nWavelength distribution (dictionary):")
    for wl, intensity in sorted(distribution.items()):
        print(f"{wl:.1f} nm: {intensity:.2f}")
    
    print("\nComplete wavelength matrix (first 10 and last 10 rows):")
    print(wavelength_matrix[:10])
    print("...")
    print(wavelength_matrix[-10:])

def plot_wavelength_distribution(wavelength_matrix):
    """
    Create an interactive Plotly graph of wavelength distribution.
    
    Args:
        wavelength_matrix (np.ndarray): 2D array with [wavelength, intensity] columns
    """
    # Create the plot
    fig = go.Figure()
    
    # Add trace
    fig.add_trace(go.Scatter(
        x=wavelength_matrix[:, 0],
        y=wavelength_matrix[:, 1],
        mode='lines',
        name='Intensity',
        line=dict(color='blue', width=2)
    ))
    
    # Update layout
    fig.update_layout(
        title='Wavelength Distribution',
        xaxis_title='Wavelength (nm)',
        yaxis_title='Intensity',
        template='plotly_white',
        hovermode='x unified'
    )
    
    # Show the plot
    fig.show()

def get_wavelength_distribution_from_image():
    """
    Get wavelength distribution from an image file and show interactive plot.
    
    Returns:
        tuple: (dict, np.ndarray) where:
            dict: {wavelength: summed_intensity} for wavelengths in range
            np.ndarray: 2D array with [wavelength, intensity] columns for all wavelengths in range
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze wavelength distribution in an image')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()
    
    # Load image
    try:
        img = Image.open(args.image_path)
        img = img.convert('RGB')  # Ensure RGB format
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Reshape to 3xN format (N = width * height)
    height, width, _ = img_array.shape
    rgb_matrix = img_array.reshape(-1, 3).T
    
    # Get wavelength distribution
    return get_wavelength_distribution(rgb_matrix)

if __name__ == "__main__":
    # If no arguments, run tests
    import sys
    if len(sys.argv) == 1:
        _test_wavelength_conversion()
        _test_wavelength_distribution()
    else:
        # Process image from command line
        dist, matrix = get_wavelength_distribution_from_image()
        if dist is not None:
            # Show interactive plot
            plot_wavelength_distribution(matrix)
