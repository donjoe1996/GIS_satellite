# import all libraries
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import os

class Image:
    def __init__(self, image_path, min_percentile=2, max_percentile=98):
        self.image_path = image_path
        self.min_percentile = min_percentile
        self.max_percentile = max_percentile

    def open_image(self):
        with rasterio.open(self.image_path) as src:
            self.image_np = src.read() # Read the raster as a numpy array
        return self.image_np

    def mask_nan_values(self):
        fill_value= -1
        image_masked = np.where(np.isnan(self.image_np), fill_value, self.image_np)

        data = np.array(image_masked)
        self.image_masked = np.ma.masked_array(data, mask=(data == fill_value))

        return self.image_masked

    def apply_scale_factor(self):
        image_ = self.image_masked * 0.0000275 + (-0.2)
        self.image_scaled = image_
        return self.image_scaled

    def stretch_data(self, min_percentile, max_percentile):
        mins = np.percentile(self.image_scaled, min_percentile, axis=(1, 2))
        maxs = np.percentile(self.image_scaled, max_percentile, axis=(1, 2))
        stretched_image = np.zeros_like(self.image_scaled, dtype=np.float32)

        for b in range(self.image_scaled.shape[0]):
            band = self.image_scaled[b, :, :]
            stretched_image[b, :, :] = (band - mins[b]) / (maxs[b] - mins[b])
            stretched_image[b, :, :] = np.clip(stretched_image[b, :, :], 0, 1)  # Ensure the values are within [0,1]

        self.image_stretched = stretched_image
        return self.image_stretched

    def create_ndvi(self):
        # Assuming the image has at least two bands: NIR (near-infrared) and Red
        # Replace these indices with the appropriate bands from your dataset
        nir_band_index = 3  # Index of NIR band (adjust as per your data)
        red_band_index = 2  # Index of Red band (adjust as per your data)

        # Extract NIR and Red bands
        nir = self.image_scaled[nir_band_index, :, :]
        red = self.image_scaled[red_band_index, :, :]

        # Calculate NDVI
        ndvi = (nir - red) / (nir + red)

        return ndvi

    def create_rgb(self, bands_order, min_value=0.90, max_value=0.96):
        """
        Combines the given bands to an RGB image and clips the values to the given range.
        Assumes that the input image is in the format (bands, rows, cols).
        The bands_order is a tuple indicating which bands to use (R, G, B).
        """

        # Get the specified bands and combine them
        # bands_order = (2,1,0)
        rgb_image = self.image_stretched[list(bands_order), :, :]
        rgb_image = np.rollaxis(rgb_image, axis=0, start=3)

        # clip to the specified range and normalize to [0,1] for display
        rgb_image_clipped_normalized = np.clip(rgb_image, min_value, max_value)
        rgb_image_clipped_normalized = (rgb_image_clipped_normalized - min_value) / (max_value - min_value)

        return rgb_image_clipped_normalized
#
# img_ = Image(r'I:\My Drive\2_geospatial_project\revalue_nature\LS8_2013.tif')
#
# a = img_.open_image()
# b = img_.mask_nan_values()
# c = img_.apply_scale_factor()
# d = img_.stretch_data(2, 98)
# e = img_.create_rgb((2,1,0))

# d.create_rgb(bands_order=(2,1,0))

# plt.figure(figsize=(10, 6))
# plt.imshow(e)
# plt.title('RGB Image with Pixel Values Clipped to [0.94, 0.98]')
# plt.axis('on')  # Hide axis labels
# plt.legend()
# plt.show()

