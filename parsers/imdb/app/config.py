import os
from pathlib import Path

INPUT_PATH = Path(
    os.environ['INPUT_DIR']
).resolve()

OUTPUT_DIR = Path(
    os.environ['OUTPUT_DIR']
).resolve()
