import glob
import os
import pandas as pd
from path.csv_loader import get_csv_folder_location, get_final_csv_folder_location, get_root_folder_location


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
    if col_h >= len(input_df.columns) or col_k >= len(input_df.columns):
        print(f"Invalid column index: col_h={col_h}, col_k={col_k} for DataFrame with columns {input_df.columns}")
        return True  # Consider it an interruption if the indices are invalid

    if (input_df.iloc[:, col_h] < 0).any() or (input_df.iloc[:, col_k] < 0).any():
        return True
    return False


def aggregate_differences(folder_path: str, col_f: int, col_h: int, col_k: int, comparison_range: int) -> list:
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
            all_differences.append((os.path.basename(file), "interrupted", comparison_range, None, None, None, None))
            continue

        differences_df = compute_differences(df, col_f, col_h, col_k, comparison_range)

        for idx, row in differences_df.iterrows():
            diff = row['Difference']
            p1_value = row[df.columns[col_h]]
            p2_value = row[df.columns[col_k]]
            all_differences.append(
                (os.path.basename(file), "success", comparison_range, diff, int(idx), p1_value, p2_value))

    return all_differences


def analysis_pipeline(col_f: int, col_h: int, col_k: int, target_range: int):
    folder_path = str(get_final_csv_folder_location())
    common_differences = aggregate_differences(folder_path, col_f, col_h, col_k, target_range)

    # Creating DataFrame for the results
    results_df = pd.DataFrame(common_differences, columns=[
        'filename', 'result', 'maximum_comparison_range', 'actual_comparison_difference',
        'row_index', 'p1_value', 'p2_value'
    ])

    # Convert row_index to integer
    results_df['row_index'] = results_df['row_index'].astype('Int64')

    # Saving results to CSV file
    results_csv_path = os.path.join(str(get_root_folder_location()), 'results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"Results saved to {results_csv_path}")


def main():
    analysis_pipeline(col_f=2, col_h=7, col_k=10, target_range=5)  # Example column indices and target range


if __name__ == "__main__":
    main()
