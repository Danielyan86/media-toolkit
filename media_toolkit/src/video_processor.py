import cv2
import numpy as np
import argparse
from pathlib import Path

# Add input source configuration
INPUT_SOURCE_DIR = Path("input_source")


def process_video(input_path, output_path, speed_factor=1.5, similarity_threshold=0.98):
    """
    Process video to speed it up and remove duplicate frames
    :param input_path: Path to input video file
    :param output_path: Path to save processed video
    :param speed_factor: Speed multiplier (default: 1.5x)
    :param similarity_threshold: Threshold for considering frames as duplicates (0-1)
    """
    # Resolve input path relative to INPUT_SOURCE_DIR if not absolute
    input_path = (
        INPUT_SOURCE_DIR / input_path
        if not Path(input_path).is_absolute()
        else input_path
    )

    # Open the video file
    cap = cv2.VideoCapture(str(input_path))  # Convert Path to string for cv2
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create video writer with adjusted FPS
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(output_path, fourcc, fps * speed_factor, (width, height))

    # Add error checking for VideoWriter
    if not out.isOpened():
        print(f"Error: Could not initialize video writer with codec avc1")
        # Fallback to mp4v if avc1 fails
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps * speed_factor, (width, height))
        if not out.isOpened():
            print("Error: Could not initialize video writer with fallback codec mp4v")
            return

    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip duplicate frames
        if prev_frame is not None:
            # Calculate similarity between current and previous frame
            similarity = np.mean(frame == prev_frame)
            if similarity > similarity_threshold:
                continue

        prev_frame = frame.copy()
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="Process video with speed adjustment and duplicate frame removal"
    )
    parser.add_argument("input", help="Input video file path")
    parser.add_argument(
        "--output",
        help="Output video file path (default: input_processed.mp4)",
        default=None,
    )
    parser.add_argument(
        "--speed", type=float, default=1.5, help="Speed factor (default: 1.5)"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.996,
        help="Similarity threshold (default: 0.98)",
    )

    args = parser.parse_args()

    # Create input source directory if it doesn't exist
    INPUT_SOURCE_DIR.mkdir(exist_ok=True)

    input_path = Path(args.input)
    if not (INPUT_SOURCE_DIR / input_path).exists() and not input_path.exists():
        print(
            f"Error: Input file not found in {INPUT_SOURCE_DIR} or as absolute path: {args.input}"
        )
        return

    # Generate output path if not specified
    output_path = args.output
    if output_path is None:
        input_stem = Path(args.input).stem
        output_path = f"{input_stem}_processed.mp4"

    process_video(args.input, output_path, args.speed, args.threshold)
    print(f"Video processing complete. Output saved to: {output_path}")


if __name__ == "__main__":
    main()
