import itertools

import pandas as pd
from path.csv_loader import load_all_csvs, load_merged_csv, get_root_folder_location
from datetime import datetime


def sanitize_df(df, comparison_range: int = 33):
    df = df[df['Type'] == 'ALL']
    # Filtering out interruptions
    df = df[(df['P1'] >= 0) & (df['P2'] >= 0)]
    df = df.copy()
    df.loc[:, "Diff"] = df["P1"] - df["P2"]
    # Filtering out only the pairs where the difference is >= comparison_range
    df = df[df['Diff'].abs() >= comparison_range]
    return df


def extract_unique_pairs(df):
    """Extract unique pairs from the sanitized dataframe."""
    unique_p1 = [float(item) for item in list(df['P1'].unique())]
    unique_p2 = [float(item) for item in list(df['P2'].unique())]
    unique_pairs = list(itertools.product(unique_p1, unique_p2))
    return sorted(unique_pairs)


def generate_pair_occurrence_matrix(merged_df: pd.DataFrame, comparison_range: int = 33):
    """Generate a pair of occurrence matrix indicating which pairs appear in which files."""
    df = sanitize_df(merged_df, comparison_range)
    unique_files = list(df['Filename'].unique())
    unique_pairs = extract_unique_pairs(df)
    pair_dict = {pair: {filename: 0 for filename in unique_files} for pair in unique_pairs}

    for filename in unique_files:
        file_df = df[df['Filename'] == filename]
        p1_values = sorted(list(file_df['P1'].tolist()))
        p2_values = sorted(list(file_df['P2'].tolist()))
        for pair in unique_pairs:
            if pair[0] in p1_values and pair[1] in p2_values:
                pair_dict[pair][filename] += 1

    debug_pair = (235.0, 202.0)
    debug_pair_occurrence = pair_dict[debug_pair]
    # Convert the pair dictionary to a DataFrame
    matrix_df = pd.DataFrame.from_dict(pair_dict, orient='index')
    matrix_df['Pair'] = matrix_df.index  # Explicitly create 'Pair' column
    matrix_df.reset_index(drop=True, inplace=True)

    print("Matrix DataFrame structure:")
    print(matrix_df.head())  # Debugging line to check the structure of matrix_df

    return matrix_df


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
    merged_csv = load_merged_csv()
    matrix_df = generate_pair_occurrence_matrix(merged_csv, comparison_range)
    pairs = find_identical_pairs(matrix_df, merged_csv)  # Pass merged_csv to find_identical_pairs
    save_results_to_csv(pairs)
    return pairs


if __name__ == "__main__":
    main()
