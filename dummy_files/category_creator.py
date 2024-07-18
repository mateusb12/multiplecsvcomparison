import pandas as pd
import random


def generate_data(h_custom=None, k_custom=None, f_all=False):
    random.seed(42)  # For reproducibility
    h_values = h_custom if h_custom else [random.randint(50, 150) for _ in range(1, 101)]
    k_values = k_custom if k_custom else [h + random.randint(-15, 35) for h in h_values]

    data = {
        'A': range(1, 101),
        'B': range(101, 201),
        'C': range(201, 301),
        'D': range(301, 401),
        'E': range(401, 501),
        'F': ['ALL' if f_all or i % 2 == 0 else 'OTHER' for i in range(1, 101)],
        'G': range(501, 601),
        'H': h_values,
        'I': range(601, 701),
        'J': range(701, 801),
        'K': k_values
    }
    return data


def create_file(file_path, h_custom=None, k_custom=None, f_all=False):
    data = generate_data(h_custom, k_custom, f_all)
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)


def create_interruption_file(file_path):
    h_custom = [i if i % 10 != 0 else -i for i in range(1, 101)]
    create_file(file_path, h_custom=h_custom)


def create_valid_file(file_path):
    create_file(file_path)


def create_matching_difference_file(file_path):
    create_file(file_path)


def create_non_matching_difference_file(file_path):
    create_file(file_path)


def create_all_rows_matching_criteria_file(file_path):
    create_file(file_path, f_all=True)


def create_partial_matching_criteria_file(file_path):
    h_custom = [i if i % 4 != 0 else i + random.randint(1, 30) for i in range(1, 101)]
    k_custom = [i + random.randint(1, 30) if i % 4 != 0 else i for i in range(1, 101)]
    create_file(file_path, h_custom=h_custom, k_custom=k_custom)
