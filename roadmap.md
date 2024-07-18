# CSV Comparison Script Goals

## Setup and Preparation

- [x] **Install necessary libraries**
  - Install `pandas`, `glob`, and `os` libraries.
  - Ensure the environment is set up correctly.

- [x] **Create dummy CSV files for testing**
  - Create a set of dummy CSV files with the required structure.
  - Ensure the files are placed in a test directory (e.g., `test_csvs/`).

## Implement Core Functionality

- [x] **Load CSV files**
  - Implement a function to load all CSV files from the specified folder.

- [x] **Compute differences**
  - Implement a function to compute differences between positive numbers in columns `H` and `K` for rows where `F == 'ALL'`.

- [x] **Handle interruptions**
  - Implement logic to skip differences when a negative number appears in columns `H` or `K`.

- [x] **Aggregate differences across files**
  - Aggregate differences from all files and find common differences matching the specified range.

## Output the Results

- [x] **Print matches**
  - Implement a function to print the matches in the specified format.

- [x] **Save results to a file**
  - Implement a function to save the results to a file for further analysis.

## Testing and Validation

- [x] **Test the script**
  - Test the script with the created dummy CSV files to ensure it works as expected.
  - Validate the results manually by cross-referencing with the CSV files.

- [x] **Optimize and refine**
  - Optimize the script for performance if dealing with a large number of files.
  - Refine the code based on any edge cases or issues encountered during testing.
