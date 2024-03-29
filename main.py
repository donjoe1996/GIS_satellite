# import all libraries
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import os

def open_image(image_path):
    with rasterio.open(image_path) as src:
        return src.read()  # Read the raster as a numpy array

def mask_nan_values(image):
    fill_value= -1
    masked_image = np.where(np.isnan(image), fill_value, image)
    return masked_image

def apply_scale_factor(image):
    image_ = image * 0.0000275 + (-0.2)
    return image_

def stretch_data(image, min_percentile, max_percentile):
    """
    Applies a linear stretch to an image based on the given percentiles.
    """
    mins = np.percentile(image, min_percentile, axis=(1, 2))
    maxs = np.percentile(image, max_percentile, axis=(1, 2))

    stretched_image = np.zeros_like(image, dtype=np.float32)

    for b in range(image.shape[0]):
        band = image[b, :, :]
        stretched_image[b, :, :] = (band - mins[b]) / (maxs[b] - mins[b])
        stretched_image[b, :, :] = np.clip(stretched_image[b, :, :], 0, 1)  # Ensure the values are within [0,1]

    return stretched_image

def combine_bands_to_rgb(image, bands_order, min_value=0.78, max_value=0.94):
    """
    Combines the given bands to an RGB image and clips the values to the given range.
    Assumes that the input image is in the format (bands, rows, cols).
    The bands_order is a tuple indicating which bands to use (R, G, B).
    """
    # Get the specified bands and combine them
    rgb_image = image[list(bands_order), :, :]
    rgb_image = np.rollaxis(rgb_image, 0, 3)

    # Clip to the specified range and normalize to [0, 1] for display
    rgb_image_clipped_normalized = np.clip(rgb_image, min_value, max_value)
    rgb_image_clipped_normalized = (rgb_image_clipped_normalized - min_value) / (max_value - min_value)

    return rgb_image_clipped_normalized

# def run():
#     IMG_PATH = r'I:\My Drive\2_geospatial_project\revalue_nature\LS8_2019.tif'
#     img = open_image(IMG_PATH)
#     img_masked = mask_nan_values(img)
#     img_scale = apply_scale_factor(img_masked)
#     img_stretch = stretch_data(img_scale, 2, 98)
#     print(img_stretch)
#
#     rgb = combine_bands_to_rgb(img_stretch, bands_order=(2,1,0))
#
#     plt.figure(figsize=(10, 6))
#     plt.imshow(rgb)
#     plt.title('RGB Image with Pixel Values Clipped to [0, 0.3]')
#     plt.axis('off')  # Hide axis labels
#     plt.show()
#
# run()


def run(folder_path):
    # List all .tif files in the folder
    tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

    # Determine the number of plots needed
    num_images = len(tif_files)
    cols = 3  # Set the number of columns for the subplot
    rows = num_images // cols + (num_images % cols > 0)  # Calculate the number of rows needed

    # Create a figure with subplots
    fig, axes = plt.subplots(rows, cols, figsize=(10, rows * 3.3))
    axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

    # Loop over each .tif file and process it
    for idx, tif_file in enumerate(tif_files):
        IMG_PATH = os.path.join(folder_path, tif_file)
        img = open_image(IMG_PATH)
        img_masked = mask_nan_values(img)
        img_scale = apply_scale_factor(img_masked)
        img_stretch = stretch_data(img_scale, 2, 98)
        rgb = combine_bands_to_rgb(img_stretch, bands_order=(2, 1, 0))

        # Display the RGB image in the subplot
        ax = axes[idx]
        ax.imshow(rgb)
        ax.set_title(os.path.basename(tif_file))
        ax.axis('off')  # Hide axis labels

    # Adjust layout
    plt.tight_layout()
    plt.show()


# Usage example:
# Set the path to the folder containing the .tif files
folder_path = r'I:\My Drive\2_geospatial_project\revalue_nature'
run(folder_path)