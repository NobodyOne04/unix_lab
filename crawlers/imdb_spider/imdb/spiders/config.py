import os
from pathlib import Path

IMDB_DIR = Path(
    os.environ['DATA_DIR']
).resolve()
