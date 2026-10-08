import os

import gdown
import pandas as pd


def load_data():
    os.makedirs("data", exist_ok=True)
    url = "https://drive.google.com/uc?id=1MOB-lzitxMdv-mju9oAUgy0LdmoAX4ql"
    file_path = "data/METABRIC_RNA_Mutation.csv"
    gdown.download(url, file_path, quiet=False)
    data = pd.read_csv(file_path, low_memory=False)
    print(data.head(10))


if __name__ == "__main__":
    load_data()
