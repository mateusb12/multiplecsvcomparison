

# Roadmap

## Pair presence search

### Goal
- Loop through the folder and find which files have the presence/absence of the pair (x, y). 
- For each pair (x, y) track the presence, absence and statistical probability

### Tasks
- [x] **Loading and sanitizing merged.csv dataframe**
- [x] **Search for (x,y) pair on several different formats**
- [x] **Filter out interruptions**
- [x] **Filter out pairs outside of the range difference criteria**
- [x] **Generate occurrence dict**
- [x] **Generate index row dict**


### Expected Result
 - A .csv file containing `P1` and `P2` values, probabilities, and the (x, y) presence or absence for each single file. 


### Expected Result Example

| P1  | P2  | Total Occurrences | Probability | IN.csv Total Occurrences | IN.csv P1 Location | IN.csv P2 Location | MidP.csv Total Occurrences | MidP.csv P1 Location | MidP.csv P2 Location | Out.csv Total Occurrences | Out.csv P1 Location | Out.csv P2 Location | PI.csv Total Occurrences | PI.csv P1 Location | PI.csv P2 Location |
|-----|-----|-------------------|-------------|--------------------------|--------------------|--------------------|---------------------------|----------------------|----------------------|--------------------------|---------------------|---------------------|--------------------------|---------------------|---------------------|
| 300 | 310 | 0                 | 0.00%       | 0                        | None               | None               | 0                         | None                 | None                 | 0                        | None                | None                | 0                        | None                | None                |



## Primitive pair generation

### Goal
- Create primitive pairs in a format that is suitable to test the pair presenc search function
- Pairs should follow a logical progression, with min_value, max_value and step

### Tasks
- [x] **Set up a minimum value**
- [x] **Set up a maximum value**
- [x] **Set up a difference value between X and Y**
- [x] **Set up a step value**

### Expected Result
 - A list of tuples in the format (x, y)

### Expected Result Example
```python
[(0, 25), (5, 30), (10, 35), (15, 40), (20, 45), (25, 50), (30, 55), (35, 60), (40, 65), (45, 70), (50, 75), (55, 80), (60, 85), (65, 90), (70, 95), (75, 100)]
```


## Extended Scanning Capabilities
### Goal
- Enhance the scanning function to detect broader differences beyond specific (x,y) pairs.

### Tasks
- [ ] **Develop an algorithm to scan entire file contents, not just specific pairs.**
- [ ] **Implement a comparison mechanism to detect variations in data across multiple files.**

### Expected Result
- A comprehensive list or report of all differences found across the files.

### Expected Result Example
- `{"file1.csv": {"line 10": "value changed from 5 to 6"}, "file2.csv": {"line 15": "value changed from 10 to 20"}}`

## Aggregate Common Differences
### Goal
- Identify and aggregate differences that frequently appear across multiple files.

### Tasks
- [ ] **Collect all differences from the extended scanning step.**
- [ ] **Count occurrences of each difference and aggregate common ones.**

### Expected Result
- A summarized list of the most frequent differences.

### Expected Result Example
- `{"difference 'value 5 to 6'": 12 occurrences, "difference 'value 10 to 20'": 8 occurrences}`

## Correlation Analysis
### Goal
- Investigate if there are correlations between identified differences and certain numerical levels or patterns.

### Tasks
- [ ] **Select statistical methods for correlation analysis (e.g., Pearson correlation, Spearman rank correlation).**
- [ ] **Apply these methods to the differences and the associated numerical levels.**

### Expected Result
- A statistical report showing correlations between differences and numerical levels.

### Expected Result Example
- A correlation matrix or scatter plot showing relationship strength between data differences and number levels.

## Analyze Data Extremes
### Goal
- Study the range or spread of data within the files by comparing the extremes of detected differences.

### Tasks
- [ ] **Determine the minimum and maximum values for each type of difference.**
- [ ] **Analyze the frequency and distribution of these extremes.**

### Expected Result
- Insights into the range and distribution of data values across files.

### Expected Result Example
- `{"minimum value difference": "0 to 5, 10 times", "maximum value difference": "70 to 75, 3 times"}`

## Capture Detailed Data
### Goal
- Create a detailed dataset from the differences detected in the .csv files.

### Tasks
- [ ] **Define data structures for storing detailed difference data.**
- [ ] **Implement data capture methods during the file scanning process.**

### Expected Result
- A detailed dataset capturing all relevant data differences.

### Expected Result Example
- A dataset or database table containing rows of detailed difference data and their occurrences.

## Perform Detailed Correlation Analysis
### Goal
- Conduct a thorough correlation analysis using the detailed data to identify potential patterns or insights.

### Tasks
- [ ] **Utilize advanced data analysis tools (like R, Python’s Pandas) to analyze the dataset.**
- [ ] **Generate reports and visualizations to illustrate findings.**

### Expected Result
- A detailed analysis report with visualizations showing data correlations.

### Expected Result Example
- Charts and graphs depicting strong and weak correlations between various data points and patterns.

## Develop Targeted Search Strategies
### Goal
- Refine the data analysis process based on identified correlations or patterns, focusing searches or filtering data accordingly.

### Tasks
- [ ] **Develop search algorithms based on identified correlations.**
- [ ] **Implement these algorithms to refine data processing and analysis.**

### Expected Result
- A refined search mechanism that focuses on significant correlations or patterns.

### Expected Result Example
- A search tool that filters and displays data based on user-specified correlation strengths or patterns.

