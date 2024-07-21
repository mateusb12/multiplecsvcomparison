import glob

import pandas as pd
from collections import Counter

from analysis.column_analysis import filter_and_process_dataframe
from path.csv_loader import get_final_csv_folder_location


def find_most_common_diff():
    folder_path = str(get_final_csv_folder_location())
    csv_files = glob.glob(f"{folder_path}/*.csv")

    merged_df = pd.DataFrame()
    for file in csv_files:
        df = pd.read_csv(file, encoding='utf-16-le', delimiter='\t')
        df = filter_and_process_dataframe(df)
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    # Diff is the difference between 3rd and 5th columns
    diff_values = merged_df["Diff"]

    if not diff_values.empty:
        most_common_diff = Counter(diff_values).most_common(1)[0][0]
    else:
        most_common_diff = None

    return most_common_diff


def main():
    most_common = find_most_common_diff()
    print(most_common)


if __name__ == "__main__":
    main()
