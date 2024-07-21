from path.csv_loader import load_all_csvs, load_merged_csv, get_root_folder_location
import pandas as pd


def sanitize_df(df):
    df = df[df['Type'] == 'ALL']
    df = df[(df['P1'] > 0) & (df['P2'] > 0)]
    df["Diff"] = df["P1"] - df["P2"]
    return df


def extract_unique_pairs(df):
    """Extract unique pairs from the sanitized dataframe."""
    unique_pairs = set()
    for index, row in df.iterrows():
        pair = (row['P1'], row['P2'])
        unique_pairs.add(pair)
    unique_pairs_list = list(unique_pairs)
    return sorted(unique_pairs_list)


def generate_pair_occurrence_matrix(merged_df: pd.DataFrame):
    """Generate a pair of occurrence matrix indicating which pairs appear in which files."""
    df = sanitize_df(merged_df)
    unique_files = df['Filename'].unique()
    unique_pairs = extract_unique_pairs(df)
    pair_dict = {pair: {filename: 0 for filename in unique_files} for pair in unique_pairs}

    for index, row in df.iterrows():
        pair = (row['P1'], row['P2'])
        if pair in pair_dict:
            pair_dict[pair][row['Filename']] = 1

    # Convert the pair dictionary to a DataFrame
    matrix_df = pd.DataFrame.from_dict(pair_dict, orient='index')
    matrix_df['Pair'] = matrix_df.index  # Explicitly create 'Pair' column
    matrix_df.reset_index(drop=True, inplace=True)

    print("Matrix DataFrame structure:")
    print(matrix_df.head())  # Debugging line to check the structure of matrix_df

    return matrix_df


def find_identical_pairs(matrix_df: pd.DataFrame):
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
            results.append({
                "Pair": pair,
                "Probability": f"{probability:.2f}%",
                "Files": ','.join(other_files)
            })
    results.sort(key=lambda x: x['Probability'], reverse=True)
    return pd.DataFrame(results)


def save_results_to_csv(df):
    csv_name = "probability_results.csv"
    path = get_root_folder_location() / csv_name
    df.to_csv(path, index=False)


def main():
    merged_csv = load_merged_csv()
    matrix_df = generate_pair_occurrence_matrix(merged_csv)
    pairs = find_identical_pairs(matrix_df)
    save_results_to_csv(pairs)
    return pairs


if __name__ == "__main__":
    main()
