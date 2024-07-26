from path.csv_loader import load_merged_csv
from probability_and_twins.probability_analysis import find_identical_pairs, generate_pair_occurrence_dict, \
    save_results_to_csv

COMPARISON_RANGE = 7


def main():
    merged_csv = load_merged_csv()
    matrix_df = generate_pair_occurrence_dict(merged_csv, (202.0, 235.0), COMPARISON_RANGE)
    pairs = find_identical_pairs(matrix_df, merged_csv)
    save_results_to_csv(pairs)


if __name__ == "__main__":
    main()
