import imageio
import os

def save_pngs_as_gif(pngs_path, output_gif_path, fps=1, repeat_count=3):
    """
    Create a GIF animation from a collection of PNG images

    Args:
        pngs_path (str): Path to the folder containing PNG images
        output_gif_path (str): Path to save the output GIF animation
        fps (int, optional): Frames per second for the GIF animation (default is 1)
        repeat_count (int, optional): Number of times the GIF animation repeats (default is 3)

    Returns:
        None
    """

    # Check if the provided folder path exists
    if not os.path.exists(pngs_path):
        raise FileNotFoundError("The folder path does not exist.")

    # Get a list of PNG files in the provided folder
    pngs_files_path = [os.path.join(pngs_path, f) for f in os.listdir(pngs_path) if f.endswith('.png')]

    # Sort the list of PNG files alphabetically
    sorted_path = sorted(pngs_files_path)

    # Create the GIF animation
    with imageio.get_writer(output_gif_path, mode='I', fps=fps) as writer:
        for _ in range(repeat_count):
            for filename in sorted_path:
                image = imageio.imread(filename)
                writer.append_data(image)

    print('Gif created succesfully at:', output_gif_path)