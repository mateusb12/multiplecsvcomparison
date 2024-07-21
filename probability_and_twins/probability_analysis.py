from path.csv_loader import load_all_csvs, load_merged_csv


def sanitize_df(df):
    df = df[df['Type'] == 'ALL']
    df = df[(df['P1'] > 0) & (df['P2'] > 0)]
    df["Diff"] = df["P1"] - df["P2"]
    return df


def check_for_twins(merged_df: pd.DataFrame):
    df = sanitize_df(merged_df)
    return


def main():
    merged_csv = load_merged_csv()
    check_for_twins(merged_csv)
    return


if __name__ == "__main__":
    main()
