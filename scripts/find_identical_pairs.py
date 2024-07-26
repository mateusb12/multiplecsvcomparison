import pandas as pd

from core.primitive_pairs import generate_primitive_pairs
from path.csv_loader import load_merged_csv
from probability_and_twins.probability_analysis import find_identical_pairs, generate_pair_occurrence_dict, \
    save_results_to_csv
from utils import move_column

COMPARISON_RANGE = 7


def main():
    merged_csv = load_merged_csv()
    primitive_pairs = generate_primitive_pairs()
    results = []
    for pair in primitive_pairs:
        p1, p2 = pair
        occurrence_dict = generate_pair_occurrence_dict(merged_csv, (p1, p2), COMPARISON_RANGE)
        pair_result = {"P1": p1, "P2": p2}
        total_occurrences = 0
        for key, value in occurrence_dict.items():
            total_occurrences += value
        probability = total_occurrences / len(occurrence_dict.keys())
        pair_result["total_occurrences"] = total_occurrences
        occurrence_dict["probability"] = probability
        for key, value in occurrence_dict.items():
            pair_result[key] = value
        results.append(pair_result)
    dataframe = pd.DataFrame(results)
    dataframe = move_column(dataframe, 'probability', 3)
    dataframe.to_csv("beta_results.csv", index=False)
    return


if __name__ == "__main__":
    main()
