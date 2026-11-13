import argparse

from etl.config import DEFAULT_TABLE, MAX_ROWS, ROOT
from etl.extract import extract
from etl.load import check_target, load_to_db, save_parquet
from etl.transform import transform
from etl.validate import validate


def parse_args():
    parser = argparse.ArgumentParser(description="ETL для датасета METABRIC")
    parser.add_argument("--table", default=DEFAULT_TABLE, help="имя таблицы в БД")
    parser.add_argument(
        "--rows",
        type=int,
        default=MAX_ROWS,
        help=f"сколько строк записать в БД, от 1 до {MAX_ROWS}",
    )
    args = parser.parse_args()
    try:
        check_target(args.table, args.rows)
    except ValueError as error:
        parser.error(str(error))
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
    print(f"Load: полный датасет сохранён в {path.relative_to(ROOT)}")

    count = load_to_db(data, args.table, args.rows)
    print(f"Load: в таблицу {args.table} записано {count} строк")


if __name__ == "__main__":
    main()
