import os
import random
from pathlib import Path
from typing import List

import pandas as pd


def get_csv_folder_location() -> Path:
    return Path(__file__).parent.parent / "dummy_files/test_csvs"


def get_final_csv_folder_location() -> Path:
    return Path(__file__).parent.parent / "csv_folder"


def get_root_folder_location() -> Path:
    return Path(__file__).parent.parent


def load_all_csvs() -> dict:
    folder = get_final_csv_folder_location()
    files = list(folder.glob("*.csv"))
    dfs = {}
    for file in files:
        df = pd.read_csv(file, encoding='utf-16-le', delimiter='\t')
        df.dropna(axis=1, how='all', inplace=True)
        df.columns = df.columns.str.strip()
        relevant_columns = ['ALL', '2024.7.15', '0.00', '00:00', '0.00.1', '00:00.1']
        df = df[relevant_columns]
        df.columns = ["Type", "Date", "P1", "Time1", "P2", "Time2"]
        filename = os.path.basename(file)
        dfs[filename] = df
    print(f"Loaded {len(dfs)} files")
    return dfs


def load_merged_csv() -> pd.DataFrame:
    folder = get_final_csv_folder_location()
    files = list(folder.glob("*.csv"))
    merged = pd.DataFrame()

    for file in files:
        filename = os.path.basename(file)
        df = pd.read_csv(file, encoding='utf-16-le', delimiter='\t')
        df.dropna(axis=1, how='all', inplace=True)

        # Standardize column names
        df.columns = df.columns.str.strip()

        # Select only the relevant columns, assuming these are the relevant columns
        relevant_columns = ['Type', 'Date', 'P1', 'Time1', 'P2', 'Time2']
        df.columns = relevant_columns
        df["Filename"] = filename
        merged = pd.concat([merged, df], ignore_index=True)

    merged.dropna(axis=1, how='all', inplace=True)
    return merged


def load_random_csv() -> pd.DataFrame:
    folder = get_csv_folder_location()
    files = list(folder.glob("*.csv"))
    file = random.choice(files)
    df = pd.read_csv(file)
    return df


def main():
    merged = load_merged_csv()
    return


if __name__ == "__main__":
    main()
