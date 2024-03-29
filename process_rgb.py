import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import os
import imageio

from img import Image

def run(image_path):

    # template img_path
    # img_path = r'I:\My Drive\2_geospatial_project\revalue_nature\LS8_2023.tif'

    # dynamic file name
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    dynamic_title = f'{base_filename}_RGB'
    output_filename = f'I:/My Drive/2_geospatial_project/revalue_nature/output/RGB/{base_filename}_RGB.png'

    img_         = Image(image_path)
    img_np       = img_.open_image()
    img_mask_nan = img_.mask_nan_values()
    img_scaled   = img_.apply_scale_factor()
    img_stretch  = img_.stretch_data(2, 98)
    img_rgb      = img_.create_rgb(bands_order=(2, 1, 0))

    plt.figure(figsize=(10, 6))
    plt.imshow(img_rgb)
    plt.title(dynamic_title)
    plt.axis('on')  # Hide axis labels
    #plt.legend()

    # save the figure
    plt.savefig(output_filename, bbox_inches='tight', pad_inches=0.1, dpi=900)  # Adjust dpi as necessary

    # image_filename = f'I:/My Drive/2_geospatial_project/revalue_nature/output/RGB.png'
    # plt.savefig(image_filename, bbox_inches='tight', pad_inches=0.1, dpi=900)  # 2400

    # plt.show()