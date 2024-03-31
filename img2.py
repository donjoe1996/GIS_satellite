from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.band_indices = []
        self.width = None
        self.height = None
        self.projection = None
        self.geotransform = None

    def open_image(self):
        self.ds = gdal.Open(self.image_path)
        if self.ds is None:
            raise ValueError("Failed to open the image file.")

        # Get metadata
        num_bands = self.ds.RasterCount
        self.width = self.ds.RasterXSize
        self.height = self.ds.RasterYSize

        # Get projection and geotransform
        self.projection = self.ds.GetProjection()
        self.geotransform = self.ds.GetGeoTransform()

        return self

    def select_bands(self, band_indices):
        self.band_indices = band_indices
        return self

    def read_selected_bands(self):
        self.band_arrays = [self.ds.GetRasterBand(idx).ReadAsArray() for idx in self.band_indices]
        return self

    def stack_bands(self):
        self.stacked_array = np.dstack(self.band_arrays)
        return self

    def apply_scale(self):
        self.stacked_array = apply_scale(self.stacked_array)

        print("Scale factor applied to image")
        return self

    def normalize(self):
        self.stacked_array = normalize_image(self.stacked_array)
        print("Image normalized")
        return self

    def clip(self, min_val=0.1, max_val=0.6):
        self.stacked_array = clip_image(self.stacked_array, min_val, max_val)
        print(f"Image clip with min value{min_val} and max value{max_val}")
        return self

    def show_image(self, output_filename, title_param, dpi_param):
        plt.figure(figsize=(8, 6))
        plt.imshow(self.stacked_array)
        plt.title(title_param)
        #plt.show()
        plt.savefig(output_filename,
                    bbox_inches='tight',
                    pad_inches=0.1,
                    dpi=dpi_param)  # Adjust dpi as necessary

        return self

    def show_image_ndvi(self, output_filename, title_param, dpi_param):

        plt.figure(figsize=(8, 6))
        plt.imshow(self.stacked_array, vmin=-0.1, vmax=0.3)

        plt.title(title_param)
        #plt.show()

        cbar = plt.colorbar()
        cbar.set_label('NDVI Values')

        plt.savefig(output_filename,
                    bbox_inches='tight',
                    pad_inches=0.1,
                    dpi=dpi_param)  # Adjust dpi as necessary

        # return self

    def calculate_ndvi(self):
        if len(self.band_arrays) != 2:
            raise ValueError("NDVI calculation requires exactly two bands (NIR and Red).")

        # Extract NIR and Red bands
        nir_band = self.band_arrays[1]  # Assuming NIR band is the first band
        red_band = self.band_arrays[0]  # Assuming Red band is the second band

        # Calculate NDVI
        ndvi = (nir_band - red_band) / (nir_band + red_band)

        self.stacked_array = ndvi

        print("NDVI calculated")
        return self

    def save_ndvi_geotiff(self, output_filename):

        # Create output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')
        ndvi_ds = driver.Create(output_filename, self.width, self.height, 1, gdal.GDT_Float32)

        # Write NDVI array to GeoTIFF band
        ndvi_band = ndvi_ds.GetRasterBand(1)
        ndvi_band.WriteArray(self.stacked_array)

        # Set geotransform (Assuming you have geotransform and projection defined elsewhere)
        # Example geotransform: (originX, pixelWidth, 0, originY, 0, pixelHeight)
        # Example projection: "EPSG:4326" (WGS 84)
        ndvi_ds.SetGeoTransform(self.geotransform)

        # Set projection
        ndvi_ds.SetProjection(self.projection)

        # Close dataset
        ndvi_ds = None

        print("NDVI geotiff saved")

def apply_scale(x):
    return x * 0.0000275 + (-0.2)

def normalize_image(image):
    min_val = np.nanmin(image)
    max_val = np.nanmax(image)
    normalized_image = (image - min_val) / (max_val - min_val)
    return np.clip(normalized_image, 0, 1)

def clip_image(image, min_val=0.1, max_val=0.6):
    rgb_image_clipped_normalized = np.clip(image, min_val, max_val)
    return (rgb_image_clipped_normalized - min_val) / (max_val - min_val)