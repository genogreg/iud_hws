import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "METABRIC_RNA_Mutation.parquet"
TABLE_NAME = "travingk"
ROWS_LIMIT = 100
DB_SETTINGS = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]


def get_engine():
    load_dotenv(ROOT / ".env")
    missing = [name for name in DB_SETTINGS if not os.getenv(name)]
    if missing:
        raise SystemExit(f"Заполните в .env: {', '.join(missing)}")

    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)


def write_to_db():
    if not DATA_PATH.exists():
        raise SystemExit("Нет файла с данными. Сначала запустите: python data_loader.py")

    data = pd.read_parquet(DATA_PATH).head(ROWS_LIMIT)
    engine = get_engine()
    data.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

    saved = pd.read_sql_table(TABLE_NAME, engine)
    engine.dispose()
    print(f"Таблица {TABLE_NAME}: {saved.shape[0]} строк, {saved.shape[1]} столбцов")
    print(saved.iloc[:5, :6].to_string(index=False))


if __name__ == "__main__":
    write_to_db()
