from analysis.column_analysis import analysis_pipeline

COMPARISON_RANGE = 20
COLUMN_F_INDEX = 5
COLUMN_H_INDEX = 7
COLUMN_K_INDEX = 10

common_differences = analysis_pipeline(COLUMN_F_INDEX, COLUMN_H_INDEX, COLUMN_K_INDEX, COMPARISON_RANGE)

