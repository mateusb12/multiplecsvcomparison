import re

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
        occurrence_dict, row_index_dict = generate_pair_occurrence_dict(merged_csv, (p1, p2), COMPARISON_RANGE)
        pair_result = {"P1": p1, "P2": p2}
        total_occurrences = 0
        for key, value in occurrence_dict.items():
            total_occurrences += value
        probability = total_occurrences / len(occurrence_dict.keys()) * 100
        pair_result["total_occurrences"] = total_occurrences
        pair_result["probability"] = f"{probability:.2f}%"
        for occurrence_key, occurrence_value in occurrence_dict.items():
            match = re.search(r'([a-zA-Z]+\.csv)$', occurrence_key)
            if match:
                tag = match.group(1)
                pair_result[f"{tag} total occurrences"] = occurrence_value
                pair_result[f"{tag} row location"] = row_index_dict[occurrence_key] + 1 if occurrence_value != 0 else "None"
        results.append(pair_result)
    dataframe = pd.DataFrame(results)
    dataframe = move_column(dataframe, 'probability', 3)
    dataframe.to_csv("beta_results.csv", index=False)
    return


if __name__ == "__main__":
    main()
