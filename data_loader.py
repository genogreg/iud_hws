import os

import gdown
import pandas as pd

DATA_URL = "https://drive.google.com/uc?id=1MOB-lzitxMdv-mju9oAUgy0LdmoAX4ql"
CSV_PATH = "data/METABRIC_RNA_Mutation.csv"
PARQUET_PATH = "data/METABRIC_RNA_Mutation.parquet"


def convert_types(data):
    data = data.copy()
    data["patient_id"] = data["patient_id"].astype("string")

    boolean_columns = [
        "chemotherapy",
        "hormone_therapy",
        "overall_survival",
        "radio_therapy",
    ]
    data[boolean_columns] = data[boolean_columns].astype("boolean")

    integer_columns = [
        "cohort",
        "neoplasm_histologic_grade",
        "lymph_nodes_examined_positive",
        "mutation_count",
        "tumor_stage",
    ]
    data[integer_columns] = data[integer_columns].astype("Int64")

    mutation_columns = [column for column in data.columns if column.endswith("_mut")]
    data[mutation_columns] = (
        data[mutation_columns]
        .fillna("0")
        .astype("string")
        .ne("0")
        .astype("boolean")
    )

    category_columns = data.select_dtypes(include=["object", "string"]).columns
    category_columns = [
        column
        for column in category_columns
        if column != "patient_id" and column not in mutation_columns
    ]
    data[category_columns] = data[category_columns].astype("category")

    return data


def load_data():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_PATH):
        gdown.download(DATA_URL, CSV_PATH, quiet=False)
    data = pd.read_csv(CSV_PATH, low_memory=False)
    data = convert_types(data)
    data.to_parquet(PARQUET_PATH, index=False)
    print(data.head(10))


if __name__ == "__main__":
    load_data()
