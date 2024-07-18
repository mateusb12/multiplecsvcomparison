import os
from category_creator import create_interruption_file, create_valid_file, create_matching_difference_file, \
    create_non_matching_difference_file, create_all_rows_matching_criteria_file, create_partial_matching_criteria_file

INTERRUPTION_FILE_AMOUNT = 1
VALID_FILE_AMOUNT = 2
MATCHING_DIFFERENCE_FILE_AMOUNT = 2
NON_MATCHING_DIFFERENCE_FILE_AMOUNT = 2
ALL_ROWS_MATCHING_CRITERIA_FILE_AMOUNT = 1
PARTIAL_MATCHING_CRITERIA_FILE_AMOUNT = 2


def create_multiple_dummy_csvs(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i in range(1, INTERRUPTION_FILE_AMOUNT + 1):
        file_path = os.path.join(folder_path, f'interruption_file_{i}.csv')
        create_interruption_file(file_path)
        print(f'Created {file_path}')

    for i in range(1, VALID_FILE_AMOUNT + 1):
        file_path = os.path.join(folder_path, f'valid_file_{i}.csv')
        create_valid_file(file_path)
        print(f'Created {file_path}')

    for i in range(1, MATCHING_DIFFERENCE_FILE_AMOUNT + 1):
        file_path = os.path.join(folder_path, f'matching_difference_file_{i}.csv')
        create_matching_difference_file(file_path)
        print(f'Created {file_path}')

    for i in range(1, NON_MATCHING_DIFFERENCE_FILE_AMOUNT + 1):
        file_path = os.path.join(folder_path, f'non_matching_difference_file_{i}.csv')
        create_non_matching_difference_file(file_path)
        print(f'Created {file_path}')

    for i in range(1, ALL_ROWS_MATCHING_CRITERIA_FILE_AMOUNT + 1):
        file_path = os.path.join(folder_path, f'all_rows_matching_criteria_file_{i}.csv')
        create_all_rows_matching_criteria_file(file_path)
        print(f'Created {file_path}')

    for i in range(1, PARTIAL_MATCHING_CRITERIA_FILE_AMOUNT + 1):
        file_path = os.path.join(folder_path, f'partial_matching_criteria_file_{i}.csv')
        create_partial_matching_criteria_file(file_path)
        print(f'Created {file_path}')


def main():
    folder_path = 'test_csvs'
    create_multiple_dummy_csvs(folder_path)


if __name__ == "__main__":
    main()
