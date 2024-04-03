from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessor:
    """
    A class for processing and visualizing images.

    Attributes:
        image_path (str): The file path to the image.
        band_indices (list): List of band indices to be selected.
        width (int): Width of the image.
        height (int): Height of the image.
        projection (str): Projection of the image.
        geotransform (tuple): Geotransform parameters of the image.
        ds (gdal.Dataset): GDAL dataset object for the image.
        band_arrays (list): List of numpy arrays containing image bands.
        stacked_array (numpy.ndarray): Stacked array of image bands.
    """

    def __init__(self, image_path):

        """
        Initialize the ImageProcessor class.

        Args:
            image_path (str): The file path to the image.
        """
        self.image_path = image_path
        self.band_indices = []
        self.width = None
        self.height = None
        self.projection = None
        self.geotransform = None
        self.ds = None
        self.band_arrays = []

    def open_image(self):
        """
             Open the image file and retrieve metadata.

             Returns:
                 ImageProcessor: The ImageProcessor object.

             Raises:
                 ValueError: If failed to open the image file.
        """
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
        """
        Select specific bands from the image.

        Args:
            band_indices (list): List of band indices to be selected.

        Returns:
            ImageProcessor: The ImageProcessor object.
        """
        self.band_indices = band_indices
        return self

    def read_selected_bands(self):
        """
        Read selected bands from the image.

        Returns:
            ImageProcessor: The ImageProcessor object.
        """
        self.band_arrays = [self.ds.GetRasterBand(idx).ReadAsArray() for idx in self.band_indices]
        return self

    def stack_bands(self):
        """
        Stack selected bands into a single array.

        Returns:
            ImageProcessor: The ImageProcessor object.
        """
        self.stacked_array = np.dstack(self.band_arrays)
        return self

    def apply_scale(self):
        """
        Apply scale factor to the image.

        Returns:
            ImageProcessor: The ImageProcessor object.
        """
        self.stacked_array = apply_scale(self.stacked_array)

        print("Scale factor applied to image")
        return self

    def normalize(self):
        """
        Normalize the image.

        Returns:
            ImageProcessor: The ImageProcessor object.
        """
        self.stacked_array = normalize_image(self.stacked_array)
        print("Image normalized")
        return self

    def clip(self, min_val=0.1, max_val=0.6):
        """
        Clip the image array.

        Args:
            min_val (float): Minimum clipping value.
            max_val (float): Maximum clipping value.

        Returns:
            ImageProcessor: The ImageProcessor object.
        """
        self.stacked_array = clip_image(self.stacked_array, min_val, max_val)
        print(f"Image clipped with min value{min_val} and max value{max_val}")
        return self

    def show_image(self, output_filename, title_param, dpi_param):
        """
        Show the image and save it to a file.

        Args:
            output_filename (str): The output filename for the image.
            title_param (str): The title for the image.
            dpi_param (int): The DPI (dots per inch) for the image.

        Returns:
            ImageProcessor: The ImageProcessor object.
        """
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
        """
        Show the NDVI image and save it to a file.

        Args:
            output_filename (str): The output filename for the NDVI image.
            title_param (str): The title for the NDVI image.
            dpi_param (int): The DPI (dots per inch) for the NDVI image.

        Returns:
            None
        """

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
        """
        Calculate Normalized Difference Vegetation Index (NDVI).

        Returns:
            ImageProcessor: The ImageProcessor object.

        Raises:
            ValueError: If the number of bands is not equal to 2.
        """
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
        """
        Save the NDVI image as a GeoTIFF file.

        Args:
            output_filename (str): The output filename for the GeoTIFF.

        Returns:
            None
        """

        # Create output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')
        ndvi_ds = driver.Create(output_filename, self.width, self.height, 1, gdal.GDT_Float32)

        # Write NDVI array to GeoTIFF band
        ndvi_band = ndvi_ds.GetRasterBand(1)
        ndvi_band.WriteArray(self.stacked_array)

        # geotransform (tuple): (originX, pixelWidth, 0, originY, 0, pixelHeight)
        # projection (string) : "EPSG:4326" (WGS 84)
        ndvi_ds.SetGeoTransform(self.geotransform)

        # Set projection
        ndvi_ds.SetProjection(self.projection)

        # Close dataset
        ndvi_ds = None

        print("NDVI geotiff saved")

def apply_scale(x):
    """
    Apply scale factor to the input array.

    Args:
        x (numpy.ndarray): Input array.

    Returns:
        numpy.ndarray: Scaled array.
    """

    return x * 0.0000275 + (-0.2)

def normalize_image(image):
    """
    Normalize the input image.

    Args:
        image (numpy.ndarray): Input image array.

    Returns:
        numpy.ndarray: Normalized image array.
    """

    min_val = np.nanmin(image)
    max_val = np.nanmax(image)
    normalized_image = (image - min_val) / (max_val - min_val)
    return np.clip(normalized_image, 0, 1)

def clip_image(image, min_val=0.1, max_val=0.6):
    """
    Clip the input image array.

    Args:
        image (numpy.ndarray): Input image array.
        min_val (float): Minimum clipping value (default: 0.1).
        max_val (float): Maximum clipping value (default: 0.6).

    Returns:
        numpy.ndarray: Clipped and normalized image array.
    """

    rgb_image_clipped_normalized = np.clip(image, min_val, max_val)
    return (rgb_image_clipped_normalized - min_val) / (max_val - min_val)