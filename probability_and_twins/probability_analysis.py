import itertools
from typing import Tuple

import pandas as pd
from path.csv_loader import load_all_csvs, load_merged_csv, get_root_folder_location
from datetime import datetime


def sanitize_df(df, comparison_range: int = 33):
    df = df[df['Type'] == 'ALL']
    df = df.copy()
    return df


def check_for_interruption(current_row, next_row, desired_pair, filename) -> bool:
    """
    Checks returns if there is any negative value between start_time and end_time.
    """
    time_dict = {current_row.P1: current_row.Time1, current_row.P2: current_row.Time2,
                 next_row.P1: next_row.Time1, next_row.P2: next_row.Time2}
    inverse_time_dict = {value: key for key, value in time_dict.items()}
    dp1, dp2 = desired_pair
    try:
        start_time = time_dict[dp1]
        end_time = time_dict[dp2]
    except KeyError:
        start_time = time_dict[current_row.P1]
        end_time = time_dict[next_row.P2]

    time_pool = [datetime.strptime(time, "%H:%M") for time in [
        current_row.Time1, current_row.Time2, next_row.Time1, next_row.Time2]]
    datetime_start_time = datetime.strptime(start_time, "%H:%M")
    datetime_end_time = datetime.strptime(end_time, "%H:%M")

    time_between_start_and_end = []
    # Check for times strictly between start_time and end_time
    for time in time_pool:
        if datetime_start_time < time < datetime_end_time:
            decoded_time = time.strftime("%H:%M")
            time_value = inverse_time_dict[decoded_time]
            time_between_start_and_end.append(time_value)

    return any(x < 0 for x in time_between_start_and_end)


def generate_pair_occurrence_dict(merged_df: pd.DataFrame, pair: Tuple[float, float], comparison_range: int = 33):
    """Generate a pair of occurrence matrix indicating which pairs appear in which files."""
    df = sanitize_df(merged_df, comparison_range)
    unique_files = list(df['Filename'].unique())
    occurrence_dict = {filename: 0 for filename in unique_files}

    for filename in unique_files:
        file_df = df[df['Filename'] == filename].reset_index(drop=False)
        p1, p2 = pair
        for index in range(len(file_df) - 1):
            current_row = file_df.iloc[index]
            current_row_pair = (float(current_row.P1), float(current_row.P2))
            while p1 not in current_row_pair:
                index += 1
                current_row = file_df.iloc[index]
                current_row_pair = (float(current_row.P1), float(current_row.P2))
            if p1 in pair and p2 in pair:
                occurrence_dict[filename] += 1
                break
            next_row = file_df.iloc[index + 1]
            next_row_pair = (float(next_row.P1), float(next_row.P2))
            current_row_pair_lowest_number = min(current_row_pair)
            next_row_pair_lowest_number = min(next_row_pair)
            if current_row_pair_lowest_number == next_row_pair_lowest_number:
                print("Found identical pair in file: " + filename)
                print(current_row)
                occurrence_dict[filename] += 1
                break
            diff = get_diff_value(current_row, next_row)
            diff_check = diff >= comparison_range
            while not diff_check:
                index += 1
                diff_search_row = file_df.iloc[index]
                diff = get_diff_value(current_row, diff_search_row)
                diff_check = diff >= comparison_range
            has_interruption = check_for_interruption(current_row, next_row, pair, filename)
            if has_interruption:
                break
            occurrence_dict[filename] += 1
            break
    return occurrence_dict


def get_diff_value(current_row: pd.Series, next_row: pd.Series) -> float:
    time_dict = {current_row.Time1: current_row.P1, current_row.Time2: current_row.P2,
                 next_row.Time1: next_row.P1, next_row.Time2: next_row.P2}
    earliest_time = min(time_dict, key=lambda x: time_dict[x])
    latest_time = max(time_dict, key=lambda x: time_dict[x])
    diff = abs(time_dict[latest_time] - time_dict[earliest_time])
    return diff


def format_date(date_str):
    """Convert date string to long date format."""
    date_obj = datetime.strptime(date_str, '%Y.%m.%d')
    return date_obj.strftime('%d %B %Y')


def find_identical_pairs(matrix_df: pd.DataFrame, original_df: pd.DataFrame):
    """Find identical pairs using the pair occurrence matrix, comparing against other files."""
    if 'Pair' not in matrix_df.columns:
        raise KeyError("'Pair' column is not found in the DataFrame")

    results = []
    total_files = matrix_df.columns.size - 1  # excluding the 'Pair' column

    for index, row in matrix_df.iterrows():
        pair = row['Pair']
        files_with_pair = row.drop('Pair')  # excluding the 'Pair' column
        other_files = files_with_pair[files_with_pair == 1].index.tolist()
        other_files_count = len(other_files)

        if other_files_count > 0:
            probability = other_files_count / total_files * 100
            p1, p2 = pair
            diff = p1 - p2
            # Extract time and date for P1 and P2 from the original dataframe
            p1_time = original_df.loc[(original_df['P1'] == p1) & (original_df['P2'] == p2), 'Time1'].values[0]
            p1_date = original_df.loc[(original_df['P1'] == p1) & (original_df['P2'] == p2), 'Date'].values[0]
            p2_time = original_df.loc[(original_df['P1'] == p1) & (original_df['P2'] == p2), 'Time2'].values[0]
            p2_date = original_df.loc[(original_df['P1'] == p1) & (original_df['P2'] == p2), 'Date'].values[0]

            # Create full timestamps
            p1_timestamp = datetime.strptime(f"{p1_date} {p1_time}", '%Y.%m.%d %H:%M')
            p2_timestamp = datetime.strptime(f"{p2_date} {p2_time}", '%Y.%m.%d %H:%M')

            dir_value = "REVERSE" if p1_timestamp > p2_timestamp else "FORWARD"
            p1_long_date = format_date(p1_date)
            p2_long_date = format_date(p2_date)
            results.append({
                "P1": int(p1),
                "P2": int(p2),
                'Diff': int(diff),
                "Probability": f"{probability:.2f}%",
                "Amount of files with this pair": other_files_count,
                "Files": ','.join(other_files),
                "DIR": dir_value,  # Add DIR value based on time comparison
                "P1_time": p1_time,
                "P1_date": p1_date,
                "P1_long_date": p1_long_date,
                "P2_time": p2_time,
                "P2_date": p2_date,
                "P2_long_date": p2_long_date
            })
    results.sort(key=lambda x: x['Probability'], reverse=True)
    return pd.DataFrame(results)


def save_results_to_csv(df):
    most_common_diff_value = df['Diff'].mode()[0]
    print(f"Most common diff value: {most_common_diff_value}")
    csv_name = "probability_results.csv"
    path = get_root_folder_location() / csv_name
    df.to_csv(path, index=False)


def main():
    comparison_range = 33
    pair = (202.0, 235.0)
    merged_csv = load_merged_csv()
    matrix_df = generate_pair_occurrence_dict(merged_csv, pair, comparison_range)
    pairs = find_identical_pairs(matrix_df, merged_csv)  # Pass merged_csv to find_identical_pairs
    save_results_to_csv(pairs)
    return pairs


if __name__ == "__main__":
    main()
