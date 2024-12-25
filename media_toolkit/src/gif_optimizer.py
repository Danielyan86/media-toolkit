from PIL import Image, ImageSequence
import os

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Input and output file paths using absolute paths
input_gif_path = os.path.join(script_dir, "DeployBotDemo.gif")
output_gif_path = os.path.join(script_dir, "DeployBotDemo_optimized.gif")

try:
    # Open input GIF
    original_gif = Image.open(input_gif_path)

    # Store unique frames
    unique_frames = []
    frame_hashes = set()

    # Iterate through all frames
    for frame in ImageSequence.Iterator(original_gif):
        # Keep original dimensions, only copy the frame
        frame_copy = frame.copy()

        frame_bytes = frame_copy.tobytes()  # Convert to byte data
        if frame_bytes not in frame_hashes:
            unique_frames.append(frame_copy)
            frame_hashes.add(frame_bytes)

    # Save the deduplicated GIF
    unique_frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=unique_frames[1:],
        optimize=True,
        loop=0,
        duration=50,
    )

    print(f"Optimized GIF saved to: {output_gif_path}")
    print(f"Original frame count: {original_gif.n_frames}")
    print(f"Frame count after deduplication: {len(unique_frames)}")

except FileNotFoundError:
    print(f"Error: Input GIF file not found at: {input_gif_path}")
    print("Please make sure the file exists in the same directory as this script.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
