import os
import re

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

from etl.config import ENV_PATH, MAX_ROWS, PARQUET_PATH

DB_SETTINGS = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]


def save_parquet(data, path=PARQUET_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(path, index=False)
    return path


def check_target(table, rows):
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", table):
        raise ValueError("Имя таблицы: только строчные латинские буквы, цифры и _")
    if not 1 <= rows <= MAX_ROWS:
        raise ValueError(f"Можно записать от 1 до {MAX_ROWS} строк")


def get_engine():
    load_dotenv(ENV_PATH)
    missing = [name for name in DB_SETTINGS if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"В .env не заполнены: {', '.join(missing)}")

    port = os.getenv("DB_PORT")
    if not port.isdigit():
        raise RuntimeError(f"DB_PORT должен быть числом, сейчас: {port}")

    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(port),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)


def load_to_db(data, table, rows=MAX_ROWS):
    check_target(table, rows)

    engine = get_engine()
    data.head(rows).to_sql(table, engine, if_exists="replace", index=False)

    with engine.connect() as connection:
        count = connection.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
    engine.dispose()
    return count
