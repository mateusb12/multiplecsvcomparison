import random
from pathlib import Path
from typing import List

import pandas as pd


def get_csv_folder_location() -> Path:
    return Path(__file__).parent.parent / "dummy_files/test_csvs"


def get_final_csv_folder_location() -> Path:
    return Path(__file__).parent.parent / "csv_folder"


def load_all_csvs() -> List[pd.DataFrame]:
    folder = get_csv_folder_location()
    files = list(folder.glob("*.csv"))
    dfs = [pd.read_csv(file) for file in files]
    return dfs


def load_random_csv() -> pd.DataFrame:
    folder = get_csv_folder_location()
    files = list(folder.glob("*.csv"))
    file = random.choice(files)
    df = pd.read_csv(file)
    return df


def main():
    all_csvs = load_all_csvs()
    return


if __name__ == "__main__":
    main()
