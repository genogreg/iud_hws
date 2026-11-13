from pathlib import Path

import gdown
import pandas as pd

DATA_URL = "https://drive.google.com/uc?id=1MOB-lzitxMdv-mju9oAUgy0LdmoAX4ql"
RAW_PATH = Path("data/METABRIC_RNA_Mutation.csv")


def extract(path=RAW_PATH):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        gdown.download(DATA_URL, str(path), quiet=False)
    return pd.read_csv(path, low_memory=False)
