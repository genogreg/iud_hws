import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

PARQUET_PATH = Path("data/METABRIC_RNA_Mutation.parquet")
MAX_ROWS = 100
DB_SETTINGS = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]


def save_parquet(data, path=PARQUET_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(path, index=False)
    return path


def get_engine():
    load_dotenv(".env")
    missing = [name for name in DB_SETTINGS if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"В .env не заполнены: {', '.join(missing)}")

    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)


def load_to_db(data, table, rows=MAX_ROWS):
    if not 1 <= rows <= MAX_ROWS:
        raise ValueError(f"Можно записать от 1 до {MAX_ROWS} строк")

    engine = get_engine()
    data.head(rows).to_sql(table, engine, if_exists="replace", index=False)

    with engine.connect() as connection:
        return connection.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar()
