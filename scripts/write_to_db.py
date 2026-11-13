import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "METABRIC_RNA_Mutation.parquet"
TABLE_NAME = "travingk"
ROWS_LIMIT = 100


def get_engine():
    load_dotenv(ROOT / ".env")
    url = URL.create(
        "postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )
    return create_engine(url)


def write_to_db():
    if not DATA_PATH.exists():
        raise SystemExit("Нет файла с данными. Сначала запустите: python data_loader.py")

    data = pd.read_parquet(DATA_PATH).head(ROWS_LIMIT)
    engine = get_engine()
    data.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

    saved = pd.read_sql_table(TABLE_NAME, engine)
    print(f"Таблица {TABLE_NAME}: {saved.shape[0]} строк, {saved.shape[1]} столбцов")
    print(saved.iloc[:5, :6].to_string(index=False))


if __name__ == "__main__":
    write_to_db()
