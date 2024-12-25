import os
import subprocess
from pathlib import Path


def convert_to_high_quality_gif(
    input_path: str,
    output_path: str = None,
    fps: int = 15,
    width: int = 1200,
    maintain_aspect_ratio: bool = True,
) -> str:
    """
    Convert video to high-quality GIF using FFmpeg with similar settings to the command:
    ffmpeg -i input.mov -vf "fps=15,scale=1200:-1:flags=lanczos" -vsync vfr output.gif

    Args:
        input_path (str): Path to input video file
        output_path (str, optional): Path for output GIF. If None, creates in same directory with '_highres.gif' suffix
        fps (int, optional): Frames per second for the output GIF. Defaults to 15
        width (int, optional): Width of the output GIF in pixels. Defaults to 1200
        maintain_aspect_ratio (bool, optional): Keep original aspect ratio. Defaults to True

    Returns:
        str: Path to the generated GIF file

    Raises:
        FileNotFoundError: If input file doesn't exist
        subprocess.CalledProcessError: If FFmpeg conversion fails
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Generate output path if not provided
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_highres.gif")

    # Prepare the height parameter
    height_param = "-1" if maintain_aspect_ratio else width

    # Construct FFmpeg command
    command = [
        "ffmpeg",
        "-i",
        input_path,
        "-vf",
        f"fps={fps},scale={width}:{height_param}:flags=lanczos",
        "-vsync",
        "vfr",
        output_path,
    ]

    try:
        # Run FFmpeg command
        subprocess.run(command, check=True, capture_output=True, text=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e.stderr}")
        raise


if __name__ == "__main__":
    # Example usage
    try:
        input_video = "path/to/your/video.mov"
        output_gif = convert_to_high_quality_gif(input_video, fps=15, width=1200)
        print(f"Successfully created GIF: {output_gif}")
    except Exception as e:
        print(f"Error: {str(e)}")
