REQUIRED_COLUMNS = [
    "patient_id",
    "age_at_diagnosis",
    "tumor_size",
    "tumor_stage",
    "lymph_nodes_examined_positive",
    "overall_survival_months",
    "overall_survival",
]


def validate(data):
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"Нет обязательных столбцов: {', '.join(missing)}")

    checks = {
        "датасет пустой": data.empty,
        "есть пустые patient_id": data["patient_id"].isna().any(),
        "есть повторяющиеся patient_id": data["patient_id"].duplicated().any(),
        "возраст вне диапазона 0–120": not data["age_at_diagnosis"].dropna().between(0, 120).all(),
        "размер опухоли не больше 0": (data["tumor_size"].dropna() <= 0).any(),
        "стадия вне диапазона 0–4": not data["tumor_stage"].dropna().between(0, 4).all(),
        "отрицательное число лимфоузлов": (data["lymph_nodes_examined_positive"].dropna() < 0).any(),
        "отрицательная длительность наблюдения": (data["overall_survival_months"].dropna() < 0).any(),
    }

    errors = [name for name, failed in checks.items() if failed]
    if errors:
        raise ValueError(f"Данные не прошли проверку: {'; '.join(errors)}")

    return data
