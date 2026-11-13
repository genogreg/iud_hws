import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
ENV_NAMES = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Читает доступы из SQLite-базы creds.db и записывает их в .env"
    )
    parser.add_argument("path", nargs="?", default="creds.db", help="путь к creds.db")
    parser.add_argument("--db", default="homeworks", help="к какой БД нужен доступ")
    return parser.parse_args()


def read_creds(path, db_name):
    if not Path(path).exists():
        raise SystemExit(f"Файл {path} не найден")

    connection = sqlite3.connect(path)
    databases = [row[0] for row in connection.execute("SELECT db_name FROM access")]
    row = connection.execute(
        "SELECT url, port, db_name, user, pass FROM access WHERE db_name = ?",
        (db_name,),
    ).fetchone()
    connection.close()

    print(f"В таблице access есть доступы к БД: {', '.join(databases)}")
    if row is None:
        raise SystemExit(f"Нет доступа к БД {db_name}")
    return row


def write_env(values):
    lines = [f"{name}='{value}'" for name, value in zip(ENV_NAMES, values)]
    ENV_PATH.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    args = parse_args()
    write_env(read_creds(args.path, args.db))
    print(f"Настройки подключения к {args.db} записаны в .env")
