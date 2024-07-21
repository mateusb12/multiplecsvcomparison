from analysis.column_analysis import analysis_pipeline

COMPARISON_RANGE = 67

ENCODING = "UTF-16-LE"
DELIMITER = "\t"

NEGATIVE_SENSITIVE_COMPARISON = True

common_differences = analysis_pipeline(COMPARISON_RANGE, ENCODING, DELIMITER, NEGATIVE_SENSITIVE_COMPARISON)
