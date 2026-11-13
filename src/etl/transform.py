BOOLEAN_COLUMNS = [
    "chemotherapy",
    "hormone_therapy",
    "overall_survival",
    "radio_therapy",
]

INTEGER_COLUMNS = [
    "cohort",
    "neoplasm_histologic_grade",
    "lymph_nodes_examined_positive",
    "mutation_count",
    "tumor_stage",
]


def transform(data):
    data = data.copy()
    data["patient_id"] = data["patient_id"].astype("string")
    data[BOOLEAN_COLUMNS] = data[BOOLEAN_COLUMNS].astype("boolean")
    data[INTEGER_COLUMNS] = data[INTEGER_COLUMNS].astype("Int64")

    mutation_columns = [column for column in data.columns if column.endswith("_mut")]
    data[mutation_columns] = (
        data[mutation_columns]
        .fillna("0")
        .astype("string")
        .ne("0")
        .astype("boolean")
    )

    text_columns = data.select_dtypes(include=["object", "string"]).columns
    category_columns = [
        column
        for column in text_columns
        if column != "patient_id" and column not in mutation_columns
    ]
    data[category_columns] = data[category_columns].astype("category")

    return data
