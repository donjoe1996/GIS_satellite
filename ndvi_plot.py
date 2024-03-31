import rasterio
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate average NDVI
def calculate_average_ndvi(ndvi_data):
    return np.nanmean(ndvi_data)

# Function to extract timestamp from file name
def extract_timestamp(filename):
    return filename.split('_')[2]  # Extracting the timestamp, assuming it's the third element after splitting by underscores

# Directory containing the NDVI raster files
ndvi_dir = '/path/to/ndvi/files/'

# List to store average NDVI values and timestamps
data = []

# Iterate over each NDVI raster file
for filename in os.listdir(ndvi_dir):
    if filename.endswith('.tif') and 'NDVI' in filename:  # Checking for '.tif' extension and 'NDVI' in filename
        with rasterio.open(os.path.join(ndvi_dir, filename)) as src:
            ndvi_data = src.read(1, masked=True)  # Read NDVI data as numpy array
            average_ndvi = calculate_average_ndvi(ndvi_data)
            timestamp = extract_timestamp(filename)
            data.append((timestamp, average_ndvi))

# Create a pandas DataFrame
df = pd.DataFrame(data, columns=['Timestamp', 'Average NDVI'])

# Convert timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Plot time series using pandas
plt.figure(figsize=(10, 6))
df.plot(x='Timestamp', y='Average NDVI', marker='o', linestyle='-')
plt.xlabel('Timestamp')
plt.ylabel('Average NDVI')
plt.title('NDVI Time Series')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
