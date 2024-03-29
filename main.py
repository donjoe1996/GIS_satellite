# import all libraries
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import os
import imageio

import process_ndvi
import process_rgb
import process_giff

print(f"Imageio version {imageio.__version__}")
print(f"Rasterio version: {rasterio.__version__}")
print(f"imageio version: {imageio.__version__}")

if __name__ == '__main__':

    # parent folder
    folder_path = r'I:\My Drive\2_geospatial_project\revalue_nature'

    # create folder to store pngs for RGB and NDVI
    os.makedirs(os.path.join(folder_path, "output/NDVI"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "output/RGB"), exist_ok=True)

    # list all .tif files in the folder
    tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

    # list all full path of .tifs files
    tif_files_path = []

    for i in tif_files:
        _ = os.path.join(folder_path, i)
        tif_files_path.append(_)

    print(tif_files)
    print(tif_files_path)

    for i in tif_files_path:

        #process_rgb.run(i)
        process_ndvi.run(i)

        pass

    # last we call on creating giff file
    # list all full path of .PNG files
    folder_path_NDVI =  r'I:\My Drive\2_geospatial_project\revalue_nature\output\NDVI'

    png_files_path = []
    NDVI_list =  [f for f in os.listdir(folder_path_NDVI) if f.endswith('.png')]

    for i in NDVI_list:
        _ = os.path.join(folder_path_NDVI, i)
        png_files_path.append(_)

    print(sorted(png_files_path))
    process_giff.run(sorted(png_files_path))


    # img_path = r'I:\My Drive\2_geospatial_project\revalue_nature\LS8_2021.tif'
    #process_ndvi.run(img_path)
    # process_rgb.run(img_path)


def run(folder_path):
    # List all .tif files in the folder
    tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

    # Determine the number of plots needed
    num_images = len(tif_files)
    cols = 3  # Set the number of columns for the subplot
    rows = num_images // cols + (num_images % cols > 0)  # Calculate the number of rows needed

    # Create a figure with subplots
    #fig, axes = plt.subplots(rows, cols, figsize=(10, rows * 3.3))
    #axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

    # Image filenames for the GIF
    image_filenames = []

    # Loop over each .tif file and process it
    for idx, tif_file in enumerate(tif_files):
#        fig, ax = plt.subplots(figsize=(10, 3.3))  # Adjust figure size as needed
        fig, ax = plt.subplots(figsize=(10, 20))  # Adjust figure size as needed

        IMG_PATH = os.path.join(folder_path, tif_file)
        img = open_image(IMG_PATH)
        img_masked = mask_nan_values(img)
        img_scale = apply_scale_factor(img_masked)
        img_stretch = stretch_data(img_scale, 2, 98)
        rgb = combine_bands_to_rgb(img_stretch, bands_order=(2, 1, 0))

        # Display the RGB image in the subplot
        #ax = axes[idx]
        ax.imshow(rgb)
        ax.set_title(os.path.basename(tif_file))
        ax.axis('off')  # Hide axis labels

        # Save the figure
        plt.tight_layout()
        image_filename = f'I:/My Drive/2_geospatial_project/revalue_nature/output/{idx}.png'
        plt.savefig(image_filename, bbox_inches='tight', pad_inches=0.1, dpi=900) #2400
        image_filenames.append(image_filename)
        # plt.close()

    # Create a GIF from the saved images
    gif_path = 'I:/My Drive/2_geospatial_project/revalue_nature/output/L8_series.gif'
    with imageio.get_writer(gif_path, mode='I', fps=1) as writer:  # Set duration here
        for filename in image_filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    print(f"GIF saved to {gif_path}")

    # Adjust layout
    plt.tight_layout()
    #plt.show()

# Usage example:
# Set the path to the folder containing the .tif files
# folder_path = r'I:\My Drive\2_geospatial_project\revalue_nature'
# run(folder_path)