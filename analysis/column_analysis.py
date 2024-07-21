import glob
import os
import pandas as pd
import traceback
from path.csv_loader import get_csv_folder_location, get_final_csv_folder_location, get_root_folder_location
from utils import print_yellow, print_red


def compute_differences(input_df: pd.DataFrame, col_f: int, col_h: int, col_k: int,
                        comparison_range: int) -> pd.DataFrame:
    col_f_name = input_df.columns[col_f]
    col_h_name = input_df.columns[col_h]
    col_k_name = input_df.columns[col_k]

    # Convert columns to numeric
    input_df[col_h_name] = pd.to_numeric(input_df[col_h_name], errors='coerce')
    input_df[col_k_name] = pd.to_numeric(input_df[col_k_name], errors='coerce')

    # Filter rows where col_f is 'ALL' and both col_h and col_k are positive numbers
    df_filtered = input_df[
        (input_df[col_f_name] == 'ALL') & (input_df[col_h_name] > 0) & (input_df[col_k_name] > 0)
        ].copy()

    df_filtered.loc[:, 'Difference'] = df_filtered[col_h_name] - df_filtered[col_k_name]
    df_matching = df_filtered[abs(df_filtered['Difference']) == comparison_range]

    return df_matching


def check_for_interruptions(input_df: pd.DataFrame, col_h: int, col_k: int) -> bool:
    if col_h >= len(input_df.columns) or col_k >= len(input_df.columns):
        print(f"Invalid column index: col_h={col_h}, col_k={col_k} for DataFrame with columns {input_df.columns}")
        return True

    try:
        col_h_data = pd.to_numeric(input_df.iloc[:, col_h], errors='coerce')
        col_k_data = pd.to_numeric(input_df.iloc[:, col_k], errors='coerce')
    except Exception as e:
        print(f"Error converting columns to numeric: {e}")
        return True

    if (col_h_data < 0).any() or (col_k_data < 0).any():
        negative_h_data_indexes = col_h_data[col_h_data < 0].index
        negative_k_data_indexes = col_k_data[col_k_data < 0].index
        print(f"Negative values found in columns H and K at indexes {negative_h_data_indexes} and "
              f"{negative_k_data_indexes}")
        return True
    return False


def aggregate_differences(folder_path: str, col_f: int, col_h: int, col_k: int, comparison_range: int,
                          encoding: str = 'utf-16-le', delimiter: str = '\t') -> list:
    all_differences = []
    csv_files = glob.glob(f"{folder_path}/*.csv")

    for file in csv_files:
        print_yellow(f"Processing file: {file}")
        try:
            df = pd.read_csv(file, encoding=encoding, delimiter=delimiter)

            # Clean the DataFrame
            df.dropna(axis=1, how='all', inplace=True)
            df.columns = [f"col_{i}" for i in range(df.shape[1])]

        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        try:
            if check_for_interruptions(df, col_h, col_k):
                print_red(f"Interruption occurred on file {file}\n")
                all_differences.append(
                    (os.path.basename(file), "interrupted", comparison_range, None, None, None, None))
                continue

            differences_df = compute_differences(df, col_f, col_h, col_k, comparison_range)

            for idx, row in differences_df.iterrows():
                diff = row['Difference']
                p1_value = row[df.columns[col_h]]
                p2_value = row[df.columns[col_k]]
                print(
                    f"Found matching difference in file {file} at line {idx}: Difference={diff}, p1_value={p1_value}, p2_value={p2_value}")
                all_differences.append(
                    (os.path.basename(file), "success", comparison_range, diff, int(idx), p1_value, p2_value))
        except Exception as e:
            tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            print(f"Error processing file {file}: {''.join(tb_str)}")
            continue

    return all_differences


def analysis_pipeline(col_f: int, col_h: int, col_k: int, target_range: int, encoding: str = 'utf-16-le',
                      delimiter: str = '\t'):
    folder_path = str(get_final_csv_folder_location())
    common_differences = aggregate_differences(folder_path, col_f, col_h, col_k, target_range, encoding, delimiter)

    results_df = pd.DataFrame(common_differences, columns=[
        'filename', 'result', 'maximum_comparison_range', 'actual_comparison_difference',
        'row_index', 'p1_value', 'p2_value'
    ])

    results_df['row_index'] = results_df['row_index'].astype('Int64')
    results_csv_path = os.path.join(str(get_root_folder_location()), 'results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"Results saved to {results_csv_path}")


def main():
    analysis_pipeline(col_f=2, col_h=7, col_k=10, target_range=5, encoding='utf-16-le', delimiter='\t')


if __name__ == "__main__":
    main()
