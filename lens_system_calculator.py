"""
Lens System Calculator

This script calculates the image position, magnification, and final image height for a system of lenses and gaps.
It uses the lens formula (1/f = 1/p + 1/q), magnification formula (M = -q/p), and image height formula (M = hi/ho).
"""
import plotly.graph_objects as go
import numpy as np

class LensResult:
    """Stores the calculation results for a single lens"""
    def __init__(self, lens_number, focal_length, object_distance, image_distance, 
                 magnification, cumulative_magnification, image_height):
        self.lens_number = lens_number
        self.focal_length = focal_length
        self.object_distance = object_distance
        self.image_distance = image_distance
        self.magnification = magnification
        self.cumulative_magnification = cumulative_magnification
        self.image_height = image_height

def calculate_image_distance(focal_length, object_distance):
    """
    Calculate the image distance (q) using the lens formula: 1/f = 1/p + 1/q.
    Returns infinity if object distance equals focal length.
    """
    if object_distance == focal_length:
        return float('inf')
    if object_distance == 0:
        return 0
    return 1 / (1 / focal_length - 1 / object_distance)

def calculate_magnification(image_distance, object_distance):
    """
    Calculate the magnification (M) using the formula: M = -q/p.
    Returns infinity if image distance is infinite.
    """
    if image_distance == float('inf'):
        return float('inf')
    if object_distance == 0:
        return float('inf')
    return -image_distance / object_distance

def calculate_image_height(object_height, magnification):
    """
    Calculate the image height (hi) using the formula: M = hi/ho.
    """
    return object_height * magnification

def process_lens_system(object_height, lenses, gaps):
    """
    Process the lens system and return a list of LensResult objects and final results.
    Returns: (results, total_magnification, final_image_position, final_image_height)
    """
    # Initialize variables
    object_distance = gaps[0]  # Initial object distance (p)
    image_height = object_height  # Initial image height (hi)
    total_magnification = 1  # Total magnification (M)
    results = []

    # Iterate through each lens
    for i, (focal_length, gap) in enumerate(zip(lenses, gaps[1:] + [0])):  # Add 0 for the last lens
        # Calculate image distance (q)
        image_distance = calculate_image_distance(focal_length, object_distance)
        
        # Calculate magnification (M) for this lens
        magnification = calculate_magnification(image_distance, object_distance)
        
        # Update total magnification
        total_magnification *= magnification
        
        # Update image height
        image_height = calculate_image_height(image_height, magnification)
        
        # Store results
        result = LensResult(
            lens_number=i + 1,
            focal_length=focal_length,
            object_distance=object_distance,
            image_distance=image_distance,
            magnification=magnification,
            cumulative_magnification=total_magnification,
            image_height=image_height
        )
        results.append(result)
        
        # Update object distance for the next lens
        object_distance = gap - image_distance

    return results, total_magnification, image_distance, image_height

def print_results(results, total_magnification, final_image_position, final_image_height):
    """Print the lens system results"""
    for result in results:
        print(f"Lens {result.lens_number}:")
        print(f"  Focal length (f): {result.focal_length} cm")
        print(f"  Object distance (p): {result.object_distance} cm")
        print(f"  Image distance (q): {result.image_distance:.2f} cm")
        print(f"  Magnification (M): {result.magnification:.2f}")
        print(f"  Cumulative Magnification: {result.cumulative_magnification:.2f}")
        print(f"  Image height (hi): {result.image_height:.2f} cm")
        print()
    
    print("Final Results:")
    print(f"  Total Magnification (M_total): {total_magnification:.2f}")
    print(f"  Final Image Position (q_final): {final_image_position:.2f} cm")
    print(f"  Final Image Height (hi_final): {final_image_height:.2f} cm")

def get_magnification_color(magnitude):
    """Return ANSI color code based on magnification magnitude"""
    if magnitude < 100:
        return ""  # No color for small values
    elif magnitude < 200:
        return "\033[93m"  # Yellow
    elif magnitude < 300:
        return "\033[33m"  # Orange
    elif magnitude < 400:
        return "\033[91m"  # Light red
    else:
        return "\033[31m"  # Bright red

def print_magnification_2d(object_height, lenses, num_lenses):
    """
    Print a 2D table of total magnification for different object distances and gap sizes.
    Both object distance and gap sizes range from 1 to 40 cm.
    Object Distance is the rows. Gap size is the columns.
    """
    gaps_list = [i * 0.05 for i in range(10, 30)]
    distance_list = [i * 0.25 for i in range(1, 30)]
    first_column_width = 6
    per_column_width = 5

    # Print header
    print(first_column_width * " " + "|", end="")
    for gap in gaps_list:
        print(f"{gap:5.2f}", end="")
    print("\n" + first_column_width * "-" + "+" + "-" * (per_column_width * len(gaps_list)))
    
    # Print table rows
    for distance in distance_list:
        print(f"{distance:5.1f} |", end="")
        for gap in gaps_list:
            # Create gaps array with equal gaps
            gaps = [distance] + [gap] * (num_lenses - 1)
            # Process the lens system
            _, total_mag, _, _ = process_lens_system(object_height, lenses, gaps)
            # Get color based on magnitude
            color_code = get_magnification_color(abs(total_mag))
            reset_code = "\033[0m" if color_code else ""
            # Print compact value
            if abs(total_mag) < 1000:
                print(f"{color_code}{total_mag:5.0f}{reset_code}", end="")
            else:
                print(f"{color_code}    ∞{reset_code}", end="")
        print()

def print_magnification_vs_distance(object_height, lenses, gaps):
    """Print the overall magnification for different object distances"""
    print("Object Distance (cm) | Total Magnification")
    print("---------------------|-------------------")
    for distance in range(1, 41):
        # Update the first gap (object distance)
        modified_gaps = [distance] + gaps[1:]
        # Process the lens system
        _, total_mag, _, _ = process_lens_system(object_height, lenses, modified_gaps)
        print(f"{distance:>19} | {total_mag:>17.2f}")

def plot_interactive_heatmap(object_height, lenses, num_lenses):
    """
    Create an interactive heatmap using Plotly showing total magnification
    for different object distances and gap sizes.
    """
    # Create ranges with better granularity
    gaps_list = np.linspace(0.1, 4, 100)  # 100 points between 0.1 and 40 cm
    distance_list = np.linspace(0.1, 40, 100)  # 100 points between 0.1 and 40 cm
    
    # Create matrix to store results
    magnification_matrix = np.zeros((len(distance_list), len(gaps_list)))
    
    # Calculate values
    for i, distance in enumerate(distance_list):
        for j, gap in enumerate(gaps_list):
            gaps = [distance] + [gap] * (num_lenses - 1)
            _, total_mag, _, _ = process_lens_system(object_height, lenses, gaps)
            # Cap very large values for better visualization
            if abs(total_mag) > 1000:
                total_mag = 1000 if total_mag > 0 else -1000
            magnification_matrix[i, j] = total_mag
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=magnification_matrix,
        x=gaps_list,
        y=distance_list,
        colorscale='RdBu',
        colorbar=dict(title='Magnification'),
        zmin=-1000,
        zmax=1000
    ))
    
    # Add layout
    fig.update_layout(
        title='Total Magnification Heatmap',
        xaxis_title='Gap Size (cm)',
        yaxis_title='Object Distance (cm)',
        width=800,
        height=800
    )
    
    # Show plot
    fig.show()

# Hardcoded values
object_height = 10  # Height of the object (ho)
lenses = [25, 25, 25, 25, 25, 25]  # Focal lengths of the lenses (f)
gaps = [2, 10, 10, 10, 10, 10]  # Distances between the object and lenses (gaps) - first is the object to lense distance, the rest are gaps

# Print 2D magnification table
print("\nMagnification Table (Object Distance vs Gap Size):")
print_magnification_2d(object_height, lenses, len(lenses))

# Show interactive heatmap
print("\nGenerating interactive heatmap...")
plot_interactive_heatmap(object_height, lenses, len(lenses))

# # Print magnification vs distance
# print("\nMagnification vs Object Distance:")
# print_magnification_vs_distance(object_height, lenses, gaps)

# # Process and print the lens system results for the original configuration
# print("\nOriginal Configuration Results:")
# results, total_mag, final_pos, final_height = process_lens_system(object_height, lenses, gaps)
# print_results(results, total_mag, final_pos, final_height)
