import sys
import os
import pandas as pd
import numpy as np

def validate_inputs(input_file, weights, impacts):
    """
    Performs strict validation on all inputs before processing.
    Returns cleaned data frames and parsed lists.
    """
    # 1. Check File Existence
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        sys.exit(1)

    # 2. Check File Extension
    if not input_file.lower().endswith('.csv'):
        print("Error: Input file must be a .csv file.")
        sys.exit(1)

    # 3. Read File
    # (We rely on pandas to fail naturally if the file is corrupted, which is standard behavior)
    df = pd.read_csv(input_file)

    # 4. Check Column Count (>= 3)
    if df.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns (1 ID column + 2 or more numeric columns).")
        sys.exit(1)

    # 5. Check Numeric Consistency
    # We select columns from 2nd index to the end
    data_part = df.iloc[:, 1:]
    
    # Check if all columns in data_part are actually numeric.
    # If a column contains a string (e.g., 'a'), pandas reads it as 'object'.
    # We check if the count of numeric columns matches the total columns.
    numeric_cols = data_part.select_dtypes(include=[np.number])
    
    if numeric_cols.shape[1] != data_part.shape[1]:
        print("Error: Columns from 2nd to last must contain numeric values only.")
        sys.exit(1)

    # 6. Parse Weights
    # Check if weights are comma-separated numbers
    weights_list = weights.split(',')
    
    # Validate each weight is a number
    # defined as a generator check
    if not all(w.replace('.', '', 1).isdigit() for w in weights_list): 
        print("Error: Weights must be numeric values separated by commas.")
        sys.exit(1)
        
    weights_arr = np.array([float(w) for w in weights_list])

    # 7. Parse Impacts
    impacts_list = impacts.split(',')
    
    # 8. Check Length Mismatch
    num_criteria = data_part.shape[1]
    
    if len(weights_arr) != num_criteria:
        print(f"Error: Number of weights ({len(weights_arr)}) does not match number of criteria ({num_criteria}).")
        sys.exit(1)
        
    if len(impacts_list) != num_criteria:
        print(f"Error: Number of impacts ({len(impacts_list)}) does not match number of criteria ({num_criteria}).")
        sys.exit(1)

    # 9. Check Impact Symbols
    allowed_impacts = {'+', '-'}
    if not set(impacts_list).issubset(allowed_impacts):
        print("Error: Impacts must be either '+' or '-'.")
        sys.exit(1)

    return df, data_part.values, weights_arr, impacts_list

def calculate_topsis(data_matrix, weights, impacts):
    """
    Performs the Vectorized TOPSIS algorithm.
    """
    # Step 1: Vector Normalization
    # sqrt of sum of squares for each column
    rss = np.sqrt(np.sum(data_matrix**2, axis=0))
    
    # Handle columns with all zeros to avoid division by zero
    rss[rss == 0] = 1 
    
    normalized_data = data_matrix / rss

    # Step 2: Weighted Normalization
    weighted_data = normalized_data * weights

    # Step 3: Determine Ideal Best and Ideal Worst
    # If impact is '+', Best is Max, Worst is Min
    # If impact is '-', Best is Min, Worst is Max
    
    ideal_best = []
    ideal_worst = []

    for i, impact in enumerate(impacts):
        col_data = weighted_data[:, i]
        if impact == '+':
            ideal_best.append(np.max(col_data))
            ideal_worst.append(np.min(col_data))
        else:
            ideal_best.append(np.min(col_data))
            ideal_worst.append(np.max(col_data))
            
    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Euclidean Distance
    # axis=1 performs summation across columns for each row
    dist_best = np.sqrt(np.sum((weighted_data - ideal_best)**2, axis=1))
    dist_worst = np.sqrt(np.sum((weighted_data - ideal_worst)**2, axis=1))

    # Step 5: Performance Score
    # Handle case where (dist_best + dist_worst) is 0
    total_dist = dist_best + dist_worst
    total_dist[total_dist == 0] = 1 
    
    scores = dist_worst / total_dist
    return scores

def topsis(input_file, weights, impacts, output_file):
    # Validate and Get Data
    df, data_matrix, weights_arr, impacts_list = validate_inputs(input_file, weights, impacts)
    
    # Calculate
    scores = calculate_topsis(data_matrix, weights_arr, impacts_list)
    
    # Append Results
    df['Topsis Score'] = scores
    # Rank: Ascending=False means higher score is Rank 1
    df['Rank'] = df['Topsis Score'].rank(ascending=False, method='min').astype(int)
    
    # Save
    df.to_csv(output_file, index=False)
    print(f"Result file saved successfully at: {output_file}")

def main():
    # 0. Argument Check
    if len(sys.argv) != 5:
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        print('Example: python topsis.py data.csv "1,1,1,1" "+,+,-,+" result.csv')
        sys.exit(1)

    # Unpack arguments
    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    # Execute
    topsis(input_file, weights, impacts, output_file)

if __name__ == "__main__":
    main()