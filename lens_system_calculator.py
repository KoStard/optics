"""
Lens System Calculator

This script calculates the image position, magnification, and final image height for a system of lenses and gaps.
It uses the lens formula (1/f = 1/p + 1/q), magnification formula (M = -q/p), and image height formula (M = hi/ho).
"""

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
    return 1 / (1 / focal_length - 1 / object_distance)

def calculate_magnification(image_distance, object_distance):
    """
    Calculate the magnification (M) using the formula: M = -q/p.
    Returns infinity if image distance is infinite.
    """
    if image_distance == float('inf'):
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

# Hardcoded values
object_height = 10  # Height of the object (ho)
lenses = [25, 25, 25, 25, 25, 25]  # Focal lengths of the lenses (f)
gaps = [2, 1, 1, 1, 1, 1]  # Distances between the object and lenses (gaps) - first is the object to lense distance, the rest are gaps

# Print magnification vs distance
print_magnification_vs_distance(object_height, lenses, gaps)

# Process and print the lens system results for the original configuration
# results, total_mag, final_pos, final_height = process_lens_system(object_height, lenses, gaps)
# print("\nOriginal Configuration Results:")
# print_results(results, total_mag, final_pos, final_height)
