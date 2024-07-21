import glob
import os
import pandas as pd
import traceback
from path.csv_loader import get_final_csv_folder_location, get_root_folder_location
from utils import print_yellow, print_red


def analysis_pipeline(target_range: int, encoding: str = 'utf-16-le',
                      delimiter: str = '\t', negative_sensitive_comparison: bool = False):
    folder_path = str(get_final_csv_folder_location())
    common_differences = aggregate_differences(folder_path, target_range, encoding, delimiter,
                                               negative_sensitive_comparison)

    results_df = pd.DataFrame(common_differences, columns=[
        'filename', 'result', 'maximum_comparison_range', 'app_index', 'p1_value', 'p2_value', 'diff'
    ])

    results_csv_path = os.path.join(str(get_root_folder_location()), 'results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"Results saved to {results_csv_path}")


def filter_and_process_dataframe(df):
    # Clean empty columns
    df.dropna(axis=1, how='all', inplace=True)
    # Rename columns
    df.columns = [f"col_{i}" for i in range(df.shape[1])]
    # Filter rows where 'col_0' is 'ALL'
    df = df[df['col_0'] == 'ALL']
    # Rename important columns
    df = df.rename(columns={'col_2': 'p1', 'col_4': 'p2'})
    # Filter rows that have negative values on either col_2 or col_3
    df = df[(df['p1'] >= 0) & (df['p2'] >= 0)]
    # Add the 'Diff' column for debugging
    df["Diff"] = df["p1"] - df["p2"]
    # FIlter rows where both p1 and p2 are zero
    df = df[(df['p1'] != 0) & (df['p2'] != 0)]
    return df


def aggregate_differences(folder_path: str, comparison_range: int,
                          encoding: str = 'utf-16-le', delimiter: str = '\t',
                          negative_sensitive_comparison: bool = False) -> list:
    all_differences = []
    csv_files = glob.glob(f"{folder_path}/*.csv")

    for file in csv_files:
        filename = os.path.basename(file)
        print_yellow(f"Processing file: {file}")
        try:
            df = pd.read_csv(file, encoding=encoding, delimiter=delimiter)
            df = filter_and_process_dataframe(df)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        try:
            # Filter only the rows where diff == comparison_range
            if not negative_sensitive_comparison:
                filtered_df = df[df['Diff'].abs() == comparison_range]
            else:
                filtered_df = df[df['Diff'] == comparison_range]
            filtered_df = filtered_df[['p1', 'p2', 'Diff']]
            app_index = filtered_df.shape[0]
            if app_index == 0:
                return all_differences
            try:
                most_common_p1, most_common_p2 = [float(item) for item in
                                                  filtered_df.groupby(['p1', 'p2']).size().idxmax()]
            except ValueError:
                most_common_p1, most_common_p2 = 0, 0
            result = "Success"
            diff = most_common_p1 - most_common_p2
            row = filename, result, comparison_range, app_index, most_common_p1, most_common_p2, diff
            all_differences.append(row)
        except Exception as e:
            tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            print(f"Error processing file {file}: {''.join(tb_str)}")
            continue

    return all_differences


def main():
    analysis_pipeline(col_f=2, col_h=7, col_k=10, target_range=5, encoding='utf-16-le', delimiter='\t')


if __name__ == "__main__":
    main()
