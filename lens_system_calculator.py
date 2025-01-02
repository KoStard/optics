"""
Lens System Calculator

This script calculates the image position, magnification, and final image height for a system of lenses and gaps.
It uses the lens formula (1/f = 1/p + 1/q), magnification formula (M = -q/p), and image height formula (M = hi/ho).

Inputs:
- object_height: Height of the object (ho).
- lenses: List of focal lengths of the lenses (f). Positive for converging, negative for diverging.
- gaps: List of distances between the lenses.

Outputs:
For each lens, it prints:
- Focal length (f)
- Object distance (p)
- Image distance (q)
- Magnification (M)
- Image height (hi)

Finally, it prints:
- Total magnification (M_total)
- Final image position (q_final)
- Final image height (hi_final)
"""

def calculate_image_distance(focal_length, object_distance):
    """
    Calculate the image distance (q) using the lens formula: 1/f = 1/p + 1/q.
    """
    return 1 / (1 / focal_length - 1 / object_distance)

def calculate_magnification(image_distance, object_distance):
    """
    Calculate the magnification (M) using the formula: M = -q/p.
    """
    return -image_distance / object_distance

def calculate_image_height(object_height, magnification):
    """
    Calculate the image height (hi) using the formula: M = hi/ho.
    """
    return object_height * magnification

def process_lens_system(object_height, lenses, gaps):
    """
    Process the lens system and calculate the final image position, magnification, and height.
    """
    # Initialize variables
    object_distance = gaps[0]  # Initial object distance (p)
    image_height = object_height  # Initial image height (hi)
    total_magnification = 1  # Total magnification (M)

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
        
        # Print results for this lens
        print(f"Lens {i + 1}:")
        print(f"  Focal length (f): {focal_length} cm")
        print(f"  Object distance (p): {object_distance} cm")
        print(f"  Image distance (q): {image_distance:.2f} cm")
        print(f"  Magnification (M): {magnification:.2f}")
        print(f"  Image height (hi): {image_height:.2f} cm")
        print()
        
        # Update object distance for the next lens
        object_distance = gap - image_distance

    # Print final results
    print("Final Results:")
    print(f"  Total Magnification (M_total): {total_magnification:.2f}")
    print(f"  Final Image Position (q_final): {image_distance:.2f} cm")
    print(f"  Final Image Height (hi_final): {image_height:.2f} cm")

# Hardcoded values
object_height = 10  # Height of the object (ho)
lenses = [25, 25, 25, 25, 25, 25]  # Focal lengths of the lenses (f)
gaps = [2, 1, 1, 1, 1, 1]  # Distances between the object and lenses (gaps) - first is the object to lense distance, the rest are gaps

# Process the lens system
process_lens_system(object_height, lenses, gaps)
