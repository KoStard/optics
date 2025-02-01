# %%
from PIL import Image
import numpy as np
import plotly.express as px

# %%
image = Image.open('experiment.jpg')
print(image.size)

# %%
hsv_array = np.array(image.convert('HSV')).reshape(-1, 3)
hsv_array = hsv_array[hsv_array[:,0] <= 270]

# %%
def get_wavelengths(hsv_array):
    """
    Returns a list of wavelengths corresponding to the HSV matrix.
    """
    # Source: https://stackoverflow.com/questions/11850105/hue-to-wavelength-mapping
    # Simple algorithm, can be improved
    return np.round(650 - 250 / 270 * hsv_array[:, 0])
wavelengths = get_wavelengths(hsv_array)

# %%
# Saturation > 50% and brightness > 33%
relevant_instances_mask = (hsv_array[:,1] > (150)) & (hsv_array[:,2] > (255/3))
wavelength_and_brightness = np.stack([wavelengths[relevant_instances_mask], hsv_array[relevant_instances_mask][:,2]], 1)
wavelength_counts = np.unique_counts(wavelengths[relevant_instances_mask])

# %%
plot = px.bar(x=wavelength_counts.values, y=wavelength_counts.counts, range_x=[400, 650], title="Wavelength Distribution", labels={"x": "Wavelength", "y": "Count"})
plot.show()
