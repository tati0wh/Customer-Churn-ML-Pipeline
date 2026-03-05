import pandas as pd
from pathlib import Path

# caminho base do projeto
BASE_DIR = Path(__file__).resolve().parents[2]

def load_train_data():
    path = BASE_DIR / "data/raw/train_churn_.csv"
    return pd.read_csv(path, sep=';', encoding='utf-8')


def load_test_data():
    path = BASE_DIR / "data/raw/test_churn_.csv"
    return pd.read_csv(path, sep=';', encoding='utf-8')


def load_sample_submission():
    path = BASE_DIR / "data/raw/sample_submission_.csv"
    return pd.read_csv(path, sep=';', encoding='utf-8')