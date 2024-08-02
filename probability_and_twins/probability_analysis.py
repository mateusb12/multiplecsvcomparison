import itertools
from typing import Tuple

import pandas as pd

from path.csv_loader import load_merged_csv, get_root_folder_location
from datetime import datetime


def sanitize_df(df, comparison_range: int = 33):
    df = df[df['Type'] == 'ALL'].copy()
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={'index': 'original_index'}, inplace=True)
    return df


def check_for_interruption_and_range(current_row, next_row, desired_pair, comparison_range, filename) -> bool:
    """
    Checks returns if there is any negative value between start_time and end_time.
    """

    def generate_permutations(input_time_dict):
        items = list(input_time_dict.items())
        pair_combinations = list(itertools.combinations(items, 2))
        return [((float(pair[0][0]), pair[0][1]), (float(pair[1][0]), pair[1][1])) for pair in pair_combinations]

    time_dict = {current_row.P1: current_row.Time1, current_row.P2: current_row.Time2,
                 next_row.P1: next_row.Time1, next_row.P2: next_row.Time2}
    inverse_time_dict = {value: key for key, value in time_dict.items()}
    time_pot = sorted(time_dict.values())
    dp1, dp2 = desired_pair
    combinations = generate_permutations(time_dict)
    pairs_meeting_threshold = [comb for comb in combinations if abs(comb[1][0] - comb[0][0]) >= comparison_range]
    non_overlapping_pairs = [comb for comb in pairs_meeting_threshold if not any(x in comb[1] for x in comb[0]) and not any(x in comb[0] for x in comb[1])]
    for pair_combination in non_overlapping_pairs:
        earliest_pair_timestamp = min(pair_combination, key=lambda x: x[0])[1]
        latest_pair_timestamp = max(pair_combination, key=lambda x: x[0])[1]
        datapoints_inbetween_earliest_and_latest = [item for item in time_pot if earliest_pair_timestamp < item < latest_pair_timestamp]
        if not datapoints_inbetween_earliest_and_latest:
            continue
        datapoint_values = [float(inverse_time_dict[item]) for item in datapoints_inbetween_earliest_and_latest]
        if any(number < 0 for number in datapoint_values):
            return False
    return True


def generate_pair_occurrence_dict(merged_df: pd.DataFrame, pair: Tuple[float, float], comparison_range: int = 33):
    """Generate a pair of occurrence matrix indicating which pairs appear in which files."""
    df = sanitize_df(merged_df, comparison_range)
    unique_files = list(df['Filename'].unique())
    occurrence_dict = {filename: 0 for filename in unique_files}
    row_index_dict = {filename: {"p1_location": 0, "p2_location": 0} for filename in unique_files}

    for filename in unique_files:
        original_df = merged_df[merged_df['Filename'] == filename].reset_index(drop=True)
        file_df = df[df['Filename'] == filename].reset_index(drop=False)
        p1, p2 = pair
        for index in range(len(file_df) - 1):
            current_row = file_df.iloc[index]
            current_row_pair = (float(current_row.P1), float(current_row.P2))
            while p1 not in current_row_pair:
                index += 1
                try:
                    current_row = file_df.iloc[index]
                except IndexError:
                    break
                current_row = file_df.iloc[index]
                current_row_pair = (float(current_row.P1), float(current_row.P2))
            if p1 in current_row_pair and p2 in current_row_pair:
                occurrence_dict[filename] += 1
                mask = (original_df['P1'] == current_row['P1']) & (original_df['P2'] == current_row['P2'])
                matching_rows = original_df[mask]
                if matching_rows.empty:
                    raise ValueError("No matching rows found")
                location = int(matching_rows.index[0] + 2)
                row_index_dict[filename] = {"p1_location": location, "p2_location": location}
                break
            next_row_index = index + 1
            try:
                next_row = file_df.iloc[next_row_index]
            except IndexError:
                break
            next_row_pair = (float(next_row.P1), float(next_row.P2))
            while p2 not in next_row_pair:
                next_row_index += 1
                try:
                    next_row = file_df.iloc[next_row_index]
                except IndexError:
                    break
                next_row_pair = (float(next_row.P1), float(next_row.P2))
            # share_same_lowest_number = check_if_share_same_lowest_number(current_row_pair, next_row_pair)
            # if share_same_lowest_number:
            #     occurrence_dict[filename] += 1
            #     break
            # diff = get_diff_value(current_row, next_row)
            # diff_check = diff >= comparison_range
            # while not diff_check:
            #     index += 1
            #     diff_search_row = file_df.iloc[index]
            #     diff = get_diff_value(current_row, diff_search_row)
            #     diff_check = diff >= comparison_range
            interruption_range_check = check_for_interruption_and_range(current_row, next_row, pair, comparison_range, filename)
            if not interruption_range_check:
                break
            occurrence_dict[filename] += 1
            p1_mask = (original_df['P1'] == current_row['P1']) & (original_df['P2'] == current_row['P2'])
            p1_matching_rows = original_df[p1_mask]
            p1_location = int(p1_matching_rows.index[0])
            # p1_location = int(current_row['original_index'])
            # p2_location = int(next_row['original_index'])
            p2_mask = (original_df['P1'] == next_row['P1']) & (original_df['P2'] == next_row['P2'])
            p2_matching_rows = original_df[p2_mask]
            p2_location = int(p2_matching_rows.index[0])
            row_index_dict[filename] = {"p1_location": p1_location + 2, "p2_location": p2_location + 2}
            break
    return occurrence_dict, row_index_dict


def check_if_share_same_lowest_number(current_row_pair, next_row_pair):
    current_row_pair_lowest_number = min(current_row_pair)
    next_row_pair_lowest_number = min(next_row_pair)
    share_same_lowest_number = current_row_pair_lowest_number == next_row_pair_lowest_number
    return share_same_lowest_number


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
    return pairs


if __name__ == "__main__":
    main()
