import glob
import os
import pandas as pd
from path.csv_loader import get_csv_folder_location, get_final_csv_folder_location


def compute_differences(input_df: pd.DataFrame, col_f: int, col_h: int, col_k: int,
                        comparison_range: int) -> pd.DataFrame:
    """
    Computes differences between positive numbers in specified columns for rows where column F equals 'ALL'.
    - Filters rows where column F equals 'ALL'
    - Ensures columns H and K contain only positive numbers
    - Computes differences between columns H and K
    - Returns a DataFrame with the differences that match the specified comparison range
    """
    col_f_name = input_df.columns[col_f]
    col_h_name = input_df.columns[col_h]
    col_k_name = input_df.columns[col_k]

    # Filter rows where column F is 'ALL' and both H and K columns contain positive numbers
    df_filtered = input_df[
        (input_df[col_f_name] == 'ALL') & (input_df[col_h_name] > 0) & (input_df[col_k_name] > 0)].copy()

    # Compute differences between columns H and K
    df_filtered.loc[:, 'Difference'] = df_filtered[col_h_name] - df_filtered[col_k_name]

    # Filter rows where the absolute difference matches the comparison range
    df_matching = df_filtered[abs(df_filtered['Difference']) == comparison_range]

    return df_matching


def check_for_interruptions(input_df: pd.DataFrame, col_h: int, col_k: int) -> bool:
    """
    Checks for interruptions by looking for negative numbers in columns H or K.
    - Returns True if any negative numbers are found, indicating an interruption
    """
    col_h_name = input_df.columns[col_h]
    col_k_name = input_df.columns[col_k]

    if (input_df[col_h_name] < 0).any() or (input_df[col_k_name] < 0).any():
        return True
    return False


def aggregate_differences(folder_path: str, col_f: int, col_h: int, col_k: int, comparison_range: int):
    """
    Aggregates differences from all files and finds common differences matching the specified range.
    - Computes differences for each file
    - Aggregates the differences
    - Finds common differences that match the specified range
    """
    all_differences = []
    csv_files = glob.glob(f"{folder_path}/*.csv")

    for file in csv_files:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        if check_for_interruptions(df, col_h, col_k):
            print(f"File {file} contains interruptions and will be skipped.")
            continue

        differences_df = compute_differences(df, col_f, col_h, col_k, comparison_range)

        for idx, row in differences_df.iterrows():
            diff = row['Difference']
            p1_value = row[df.columns[col_h]]
            p2_value = row[df.columns[col_k]]
            all_differences.append((os.path.basename(file), idx, diff, p1_value, p2_value))

    return all_differences


def analysis_pipeline(col_f: int, col_h: int, col_k: int, target_range: int):
    folder_path = str(get_final_csv_folder_location())
    common_differences = aggregate_differences(folder_path, col_f, col_h, col_k, target_range)


def main():
    folder_path = str(get_csv_folder_location())
    target_range = 20
    col_f, col_h, col_k = 5, 7, 10

    common_differences = aggregate_differences(folder_path, col_f, col_h, col_k, target_range)
    for file, idx, diff, p1_value, p2_value in common_differences:
        print(f"[File] → {file} | [Maximum Comparison Range] → {target_range} | [Actual Comparison Difference] → {diff}"
              f" | [Row Index] → {idx} | [P1 Value] → {p1_value} | [P2 Value] → {p2_value}")


if __name__ == "__main__":
    main()
