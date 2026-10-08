import os

import gdown
import pandas as pd


def convert_types(data):
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
    data[mutation_columns] = data[mutation_columns].astype("string")

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
    url = "https://drive.google.com/uc?id=1MOB-lzitxMdv-mju9oAUgy0LdmoAX4ql"
    file_path = "data/METABRIC_RNA_Mutation.csv"
    parquet_path = "data/METABRIC_RNA_Mutation.parquet"
    gdown.download(url, file_path, quiet=False)
    data = pd.read_csv(file_path, low_memory=False)
    data = convert_types(data)
    data.to_parquet(parquet_path, index=False)
    print(data.head(10))


if __name__ == "__main__":
    load_data()
