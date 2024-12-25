# Media Toolkit

A Python-based media processing toolkit for handling video and image transformations.

## Project Structure

```
media_toolkit/
├── src/                    # Source code
│   ├── __init__.py
│   ├── video_processor.py  # Video processing modules
│   └── gif_builer.py      # GIF generation modules
├── tests/                  # Test files
├── config/                 # Configuration files
├── media/                  # Media files (gitignored)
│   ├── source/            # Source media files
│   └── output/            # Generated media files
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Place source media files in `media/source/` directory
3. Generated files will be saved in `media/output/` directory

## Features

- Video processing and transformation
- GIF generation from videos
- More features coming soon...

## Usage

Import and use the modules from the `src` directory:

```python
from src.video_processor import process_video
from src.gif_builer import create_gif
```

## Note

Media files in `media/source/` and `media/output/` directories are gitignored to keep the repository clean.
