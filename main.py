# import all libraries
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import os
import imageio

import process_ndvi
import process_rgb
import process_false_composite
import process_giff

print(f"Numpy version {np.__version__}")
print(f"Rasterio version: {rasterio.__version__}")
print(f"imageio version: {imageio.__version__}")

if __name__ == '__main__':

    # parent folder
    folder_path = r'I:\My Drive\2_geospatial_project\revalue_nature'

    # create folder to store pngs for RGB and NDVI
    os.makedirs(os.path.join(folder_path, "output/NDVI"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "output/NDVI_geotiff"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "output/RGB"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "output/FalseComposite"), exist_ok=True)

    # list all .tif files in the folder
    tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

    # list all full path of .tifs files
    tif_files_path = []

    for i in tif_files:
        _ = os.path.join(folder_path, i)
        tif_files_path.append(_)

    print(tif_files)
    print(tif_files_path)


    # Run RGB, NDVI, and false composite
    for i in tif_files_path:

        process_rgb.run(i)
        process_ndvi.run(i)
        process_false_composite.run(i)


    # create gif for NDVI
    NDVI_pngs = r'I:\My Drive\2_geospatial_project\revalue_nature\output\NDVI'
    NDVI_output_gif_path = r'I:\My Drive\2_geospatial_project\revalue_nature\output\L8_NDVI_GIF.gif'
    process_giff.save_pngs_as_gif(NDVI_pngs, NDVI_output_gif_path)

    # #create gif for RGB
    RGB_pngs = r'I:\My Drive\2_geospatial_project\revalue_nature\output\RGB'
    RGB_output_gif_path = r'I:\My Drive\2_geospatial_project\revalue_nature\output\L8_RGB_GIF.gif'
    process_giff.save_pngs_as_gif(RGB_pngs, RGB_output_gif_path)

    #create gif for FalseComposite
    false_composite_pngs = r'I:\My Drive\2_geospatial_project\revalue_nature\output\FalseComposite'
    false_composite_output_gif_path = r'I:\My Drive\2_geospatial_project\revalue_nature\output\L8_FalseComposte_GIF.gif'
    process_giff.save_pngs_as_gif(false_composite_pngs, false_composite_output_gif_path)