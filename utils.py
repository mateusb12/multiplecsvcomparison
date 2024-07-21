def print_yellow(text: str):
    print(f"\033[93m{text}\033[0m")


def print_red(text: str):
    print(f"\033[91m{text}\033[0m")


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
