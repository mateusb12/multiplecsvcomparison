import pandas as pd
import os


def create_dummy_csv(file_path):
    # Define the structure of the dummy CSV file
    data = {
        'A': range(1, 101),
        'B': range(101, 201),
        'C': range(201, 301),
        'D': range(301, 401),
        'E': range(401, 501),
        'F': ['ALL' if i % 2 == 0 else 'OTHER' for i in range(1, 101)],
        'G': range(501, 601),
        'H': [i if i % 10 != 0 else -i for i in range(1, 101)],
        'I': range(601, 701),
        'J': range(701, 801),
        'K': [i * 2 for i in range(1, 101)]
    }

    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)


def create_multiple_dummy_csvs(folder_path, num_files):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i in range(1, num_files + 1):
        file_path = os.path.join(folder_path, f'dummy_file_{i}.csv')
        create_dummy_csv(file_path)
        print(f'Created {file_path}')


if __name__ == "__main__":
    create_multiple_dummy_csvs('test_csvs', 10)
