import argparse

from etl.extract import extract
from etl.load import MAX_ROWS, load_to_db, save_parquet
from etl.transform import transform
from etl.validate import validate


def parse_args():
    parser = argparse.ArgumentParser(description="ETL для датасета METABRIC")
    parser.add_argument("--table", default="travingk", help="имя таблицы в БД")
    parser.add_argument(
        "--rows",
        type=int,
        default=MAX_ROWS,
        help=f"сколько строк записать в БД, от 1 до {MAX_ROWS}",
    )
    args = parser.parse_args()
    if not 1 <= args.rows <= MAX_ROWS:
        parser.error(f"--rows должен быть от 1 до {MAX_ROWS}")
    return args


def main():
    args = parse_args()

    raw = extract()
    print(f"Extract: {raw.shape[0]} строк, {raw.shape[1]} столбцов")

    data = transform(raw)
    print("Transform: типы данных приведены")

    validate(data)
    print("Validate: проверки пройдены")

    path = save_parquet(data)
    print(f"Load: полный датасет сохранён в {path}")

    count = load_to_db(data, args.table, args.rows)
    print(f"Load: в таблицу {args.table} записано {count} строк")


if __name__ == "__main__":
    main()
