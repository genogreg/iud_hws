from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_URL = "https://drive.google.com/uc?id=1MOB-lzitxMdv-mju9oAUgy0LdmoAX4ql"
RAW_PATH = ROOT / "data" / "METABRIC_RNA_Mutation.csv"
PARQUET_PATH = ROOT / "data" / "METABRIC_RNA_Mutation.parquet"
ENV_PATH = ROOT / ".env"
DEFAULT_TABLE = "travingk"
MAX_ROWS = 100
