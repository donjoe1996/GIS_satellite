"""
Module to run RGB processing on satellite images and save the result as a PNG.

This script processes satellite images to display RGB images and saves the result as a PNG file.

Author: [Author Name]

"""

import os
from img2 import ImageProcessor

def run(image_path):
    """
    Run RGB processing on the specified satellite image.

    Args:
        image_path (str): The file path to the input satellite image.

    Returns:
        None
    """

    # dynamic file name
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    dynamic_title = f'{base_filename}_RGB'
    output_filename = f'I:/My Drive/2_geospatial_project/revalue_nature/output/RGB/{base_filename}_RGB.png'

    # Process image
    img_ = (
        ImageProcessor(image_path)
        .open_image()
        .select_bands([3, 2, 1])
        .read_selected_bands()
        .stack_bands()
        .apply_scale()
        .normalize()
        .clip()
        .show_image(output_filename, dynamic_title, 1200)
    )

