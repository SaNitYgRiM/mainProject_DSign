import os
from PIL import Image

def gif_to_frames(gif_path, output_dir):
    gif = Image.open(gif_path)
    gif.seek(0)
    frame_number = 0
    while True:
        try:
            frame = gif.copy()
            frame_path = os.path.join(output_dir, f"{frame_number}.jpg")
            frame = frame.convert("RGB")  # Convert to RGB mode before saving
            frame.save(frame_path)
            frame_number += 1
            gif.seek(gif.tell() + 1)
        except EOFError:
            break

def process_gif_directory(gif_directory, output_directory):
    for file_name in os.listdir(gif_directory):
        gif_path = os.path.join(gif_directory, file_name)
        gif_name = os.path.splitext(file_name)[0]
        gif_output_dir = os.path.join(output_directory, gif_name)
        os.makedirs(gif_output_dir, exist_ok=True)  # Create a folder for each GIF
        gif_to_frames(gif_path, gif_output_dir)

if __name__ == "__main__":
    # Input directory containing GIFs
    gif_directory = "ISLvideoGifs"

    # Output directory to save frames
    output_directory = "DATA_PATH/All_Frames"

    process_gif_directory(gif_directory, output_directory)
