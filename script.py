from analysis.column_analysis import analysis_pipeline

COMPARISON_RANGE = 20

COLUMN_F_INDEX = 1
COLUMN_H_INDEX = 3
COLUMN_K_INDEX = 4

ENCODING = "UTF-16-LE"
DELIMITER = "\t"

common_differences = analysis_pipeline(COLUMN_F_INDEX, COLUMN_H_INDEX, COLUMN_K_INDEX, COMPARISON_RANGE, ENCODING,
                                       DELIMITER)
