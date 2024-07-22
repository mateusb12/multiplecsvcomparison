from path.csv_loader import load_merged_csv
from probability_and_twins.probability_analysis import find_identical_pairs, generate_pair_occurrence_matrix, \
    save_results_to_csv

COMPARISON_RANGE = 67
NEGATIVE_SENSITIVE_COMPARISON = False


def main():
    merged_csv = load_merged_csv()
    matrix_df = generate_pair_occurrence_matrix(merged_csv, NEGATIVE_SENSITIVE_COMPARISON)
    pairs = find_identical_pairs(matrix_df)
    pairs = pairs[pairs['Diff'] == COMPARISON_RANGE] if NEGATIVE_SENSITIVE_COMPARISON \
        else pairs[pairs['Diff'].abs() == COMPARISON_RANGE]
    save_results_to_csv(pairs)


if __name__ == "__main__":
    main()
