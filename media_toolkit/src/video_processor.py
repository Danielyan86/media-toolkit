import cv2
import numpy as np
import argparse
from pathlib import Path


def process_video(input_path, output_path, speed_factor=1.5, similarity_threshold=0.98):
    """
    Process video to speed it up and remove duplicate frames
    :param input_path: Path to input video file
    :param output_path: Path to save processed video
    :param speed_factor: Speed multiplier (default: 1.5x)
    :param similarity_threshold: Threshold for considering frames as duplicates (0-1)
    """
    # Open the video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create video writer with adjusted FPS
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps * speed_factor, (width, height))

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
    parser.add_argument("output", help="Output video file path")
    parser.add_argument(
        "--speed", type=float, default=1.5, help="Speed factor (default: 1.5)"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.98,
        help="Similarity threshold (default: 0.98)",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {args.input} does not exist")
        return

    process_video(args.input, args.output, args.speed, args.threshold)
    print(f"Video processing complete. Output saved to: {args.output}")


if __name__ == "__main__":
    main()
