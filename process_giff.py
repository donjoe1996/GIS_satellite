import imageio

def run(image_filenames_param):

    # list of pngs files
    image_filenames = image_filenames_param

    # ouput location to store gif file
    output_path = 'I:/My Drive/2_geospatial_project/revalue_nature/output/L8_NDVI_GIF.gif'

    # create gif file
    with imageio.get_writer(output_path, mode='I', fps=1) as writer:
        for _ in range(2):  # Set repeat_count to control how many times the GIF repeats
            for filename in image_filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

    print('Giff created')

