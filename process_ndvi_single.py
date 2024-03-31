import matplotlib.pyplot as plt
import os
from img import Image
from matplotlib.colors import ListedColormap


img_path = r'I:\My Drive\2_geospatial_project\revalue_nature\LS8_2023_masked.tif'

# call img library
img_         = Image(img_path)
img_np       = img_.open_im()
img_mask_nan = img_.mask_nan_values()
img_scaled   = img_.apply_scale_factor()
img_stretch  = img_.stretch_data(2, 98)
img_ndvi     = img_.create_ndvi()


# plot figure
plt.figure(figsize=(10, 6))
plt.imshow(img_ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.title('NDVI')
plt.axis('on')
# plt.legend()

# Add colorbar with values
cbar = plt.colorbar()
cbar.set_label('NDVI Values')

plt.show()

print('aaaa')
# save the figure
#plt.savefig(output_filename, bbox_inches='tight', pad_inches=0.1, dpi=900)  # Adjust dpi as necessary
