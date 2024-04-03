"""
Module to run NDVI calculation on satellite images and save results as PNG and GeoTIFF.

This script processes satellite images to calculate Normalized Difference Vegetation Index (NDVI)
and saves the result as a PNG image and a GeoTIFF file.

Author: [Author Name]

"""

import os
from img2 import ImageProcessor

def run(image_path):
    """
    Run NDVI calculation on the specified satellite image.

    Args:
        image_path (str): The file path to the input satellite image.

    Returns:
        None
    """

    # variable for plotting
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    dynamic_title = f'{base_filename}_NDVI'
    output_filename = f'I:/My Drive/2_geospatial_project/revalue_nature/output/NDVI/{base_filename}_NDVI.png'

    # variable for .tif file
    output_filename_tiff = f'I:/My Drive/2_geospatial_project/revalue_nature/output/NDVI_geotiff/{base_filename}_NDVI.tif'

    # process the image
    img_ = (
        ImageProcessor(image_path)
        .open_image()
        .select_bands([3, 4]) # order [red, nir]
        .read_selected_bands()
        .stack_bands()
        .apply_scale()
        #.normalize()
        .calculate_ndvi()
        .save_ndvi_geotiff(output_filename_tiff)
    )

    # display NDVI image
    img_2 = (
        ImageProcessor(image_path)
        .open_image()
        .select_bands([3, 4]) # order [red, nir]
        .read_selected_bands()
        .stack_bands()
        .apply_scale()
        #.normalize()
        .calculate_ndvi()
        .show_image_ndvi(output_filename, dynamic_title, 1200)
    )

