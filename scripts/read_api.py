from pathlib import Path

import pandas as pd
import requests

API_URL = "https://api.fda.gov/drug/event.json"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "openfda_events.parquet"


def join_values(items, key):
    values = [item.get(key) for item in items if item.get(key)]
    return ", ".join(dict.fromkeys(values))


def read_api():
    params = {"limit": 100, "sort": "receivedate:desc"}
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    reports = response.json()["results"]

    rows = []
    for report in reports:
        patient = report.get("patient", {})
        drugs = patient.get("drug", [])
        reactions = patient.get("reaction", [])

        rows.append(
            {
                "report_id": report.get("safetyreportid"),
                "received_date": report.get("receivedate"),
                "country": report.get("occurcountry"),
                "serious": report.get("serious"),
                "patient_age": patient.get("patientonsetage"),
                "age_unit": patient.get("patientonsetageunit"),
                "patient_sex": patient.get("patientsex"),
                "patient_weight": patient.get("patientweight"),
                "drug_names": join_values(drugs, "medicinalproduct"),
                "drug_indications": join_values(drugs, "drugindication"),
                "reactions": join_values(reactions, "reactionmeddrapt"),
                "reaction_outcomes": join_values(reactions, "reactionoutcome"),
                "drug_count": len(drugs),
                "reaction_count": len(reactions),
            }
        )

    data = pd.DataFrame(rows)
    data["received_date"] = pd.to_datetime(
        data["received_date"], format="%Y%m%d", errors="coerce"
    )
    data["serious"] = data["serious"].eq("1").astype("boolean")
    data["patient_age"] = pd.to_numeric(data["patient_age"], errors="coerce")
    data["patient_weight"] = pd.to_numeric(data["patient_weight"], errors="coerce")
    data[["drug_count", "reaction_count"]] = data[
        ["drug_count", "reaction_count"]
    ].astype("Int64")
    data[["country", "age_unit", "patient_sex"]] = data[
        ["country", "age_unit", "patient_sex"]
    ].astype("category")

    DATA_PATH.parent.mkdir(exist_ok=True)
    data.to_parquet(DATA_PATH, index=False)

    preview_columns = [
        "report_id",
        "received_date",
        "country",
        "serious",
        "patient_age",
        "patient_sex",
        "drug_count",
        "reaction_count",
    ]
    print(data[preview_columns].head(15).to_string(index=False))

    return data


if __name__ == "__main__":
    read_api()
