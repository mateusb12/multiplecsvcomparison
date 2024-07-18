import pandas as pd

from path.csv_loader import load_random_csv


def compute_differences(input_df: pd.DataFrame, col_f: int, col_h: int, col_k: int) -> pd.Series:
    """
    This function computes differences between positive numbers in specified columns for rows where a specified column equals 'ALL'.
    - It filters the rows where the specified column value is 'ALL'
    - Then it ensures that the specified columns contain only positive numbers
    - Finally, it computes the differences between the specified columns
    - In the end, it returns the differences as a pandas Series
    """
    df_filtered = input_df[input_df.iloc[:, col_f] == 'ALL']

    df_filtered = df_filtered[(df_filtered.iloc[:, col_h] > 0) & (df_filtered.iloc[:, col_k] > 0)]
    differences = df_filtered.iloc[:, col_h] - df_filtered.iloc[:, col_k]

    return differences


def main():
    random_df = load_random_csv()
    differences = compute_differences(random_df, col_f=5, col_h=7, col_k=10)
    print(differences)
    return differences


if __name__ == "__main__":
    main()
