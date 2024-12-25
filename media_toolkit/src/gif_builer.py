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

    # 存储唯一帧
    unique_frames = []
    frame_hashes = set()

    # 遍历所有帧
    for frame in ImageSequence.Iterator(original_gif):
        # 保持原始尺寸，只复制帧
        frame_copy = frame.copy()

        frame_bytes = frame_copy.tobytes()  # 转换为字节数据
        if frame_bytes not in frame_hashes:
            unique_frames.append(frame_copy)
            frame_hashes.add(frame_bytes)

    # 保存去重后的 GIF
    unique_frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=unique_frames[1:],
        optimize=True,
        loop=0,
        duration=50,
    )

    print(f"优化后的 GIF 已保存到: {output_gif_path}")
    print(f"原始帧数: {original_gif.n_frames}")
    print(f"去重后帧数: {len(unique_frames)}")

except FileNotFoundError:
    print(f"Error: Input GIF file not found at: {input_gif_path}")
    print("Please make sure the file exists in the same directory as this script.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
