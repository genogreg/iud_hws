# iud_hws
Тут анализ будет датасета с клиническими и генетическими признаками с раком груди

Датасет: https://drive.google.com/file/d/1MOB-lzitxMdv-mju9oAUgy0LdmoAX4ql/view?usp=share_link


- Количество пациентов: 1 904
- Количество признаков: 693
- Клинические признаки: 31
- Признаки экспрессии мРНК: 331 ген
- Признаки мутаций: 175 генов

Датасет содержит клинические, категориальные, числовые и генетические
признаки, а также пропущенные значения.

## Запуск

Создать окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Файл `requirements.txt` содержит все библиотеки проекта:

- `gdown`, `pandas`, `pyarrow` — загрузка датасета и сохранение в Parquet;
- `requests` — запросы к openFDA API;
- `sqlalchemy`, `psycopg2-binary`, `python-dotenv` — запись в PostgreSQL
  и чтение настроек подключения из `.env`;
- `jupyter`, `matplotlib`, `seaborn`, `plotly`, `kaleido` — EDA и графики.

Запустить загрузку датасета:

```bash
python data_loader.py
```

Скрипт скачивает датасет, приводит типы данных и сохраняет результат в
`data/METABRIC_RNA_Mutation.parquet`.

## Запись в базу данных

Скрипт `scripts/write_to_db.py` берёт первые 100 строк обработанного
датасета и записывает их в PostgreSQL в таблицу `travingk`. Если таблица
уже есть, она перезаписывается.

Данные для подключения хранятся только в файле `.env`, который добавлен в
`.gitignore`. Шаблон без значений лежит в `.env.example`:

```bash
cp .env.example .env
```

В `.env` нужно заполнить `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` и
`DB_PASSWORD`.

Запуск из корня репозитория (после `python data_loader.py`):

```bash
python scripts/write_to_db.py
```

После записи скрипт читает таблицу обратно и выводит её размер и первые
строки.
