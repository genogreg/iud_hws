import gdown
import pandas as pd

from etl.config import DATA_URL, RAW_PATH


def extract(path=RAW_PATH):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        part_path = path.with_suffix(".part")
        gdown.download(DATA_URL, str(part_path), quiet=False)
        part_path.rename(path)
    return pd.read_csv(path, low_memory=False)
