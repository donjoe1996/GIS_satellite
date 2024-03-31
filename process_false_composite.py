import os

from img import Image
from img2 import ImageProcessor

def run(image_path):

    # dynamic file name
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    dynamic_title = f'{base_filename}_FalseComposite'
    output_filename = f'I:/My Drive/2_geospatial_project/revalue_nature/output/FalseComposite/{base_filename}_FalseComposte.png'

    img_ = (
        ImageProcessor(image_path)
        .open_image()
        .select_bands([4, 3, 2])
        .read_selected_bands()
        .stack_bands()
        .apply_scale()
        .normalize()
        .clip()
        .show_image(output_filename, dynamic_title, 1200)
    )

