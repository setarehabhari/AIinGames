import os
import re
import numpy as np
from collections import defaultdict

# Calculates win rates with sd for each model against other models

# Initialize a dictionary to hold win rates between pairs of models
model_combinations = defaultdict(list)

# Adjust this path to where your result files are stored
folder_path = "./"

# Read each result file
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), "r") as f:
            lines = f.readlines()
            for line in lines:
                # Regex to capture win rates for player 0 and player 1
                match = re.match(r"Win Rate - Player 0: ([0-9.]+), Player 1: ([0-9.]+)", line)
                if match:
                    rate0, rate1 = float(match[1]), float(match[2])

                    # Extract the models
                    model0_match = re.search(r"Models: \['([^']+)", lines[1])
                    model1_match = re.search(r", '([^']+)'\]", lines[1])

                    if model0_match and model1_match:
                        model0 = model0_match[1]
                        model1 = model1_match[1]

                        # Store the win rates for the pair of models (mirror the results)
                        model_combinations[(model0, model1)].append(rate0)
                        model_combinations[(model1, model0)].append(rate1)  # Include the reverse pair too

# Now calculate the average win rates and standard deviations for each model against every other model
model_names = sorted(set([model for pair in model_combinations.keys() for model in pair]))  # List of unique models
win_rate_matrix = np.zeros((len(model_names), len(model_names)), dtype=object)  # Initialize the win rate matrix with objects to store strings

# Fill the matrix with avg win rates and SD as formatted strings
for i, model1 in enumerate(model_names):
    for j, model2 in enumerate(model_names):
        if (model1, model2) in model_combinations:
            avg_rate = np.mean(model_combinations[(model1, model2)])
            std_dev = np.std(model_combinations[(model1, model2)])
            # Format the result as 'Avg Win Rate ± Std Dev'
            win_rate_matrix[i, j] = f"{avg_rate:.4f} ± {std_dev:.4f}"

# Mirror the values (ensure the matrix is symmetric)
for i in range(len(model_names)):
    for j in range(i + 1, len(model_names)):
        win_rate_matrix[j, i] = win_rate_matrix[i, j]  # Make sure model i vs model j is the same as model j vs model i

# Print out the results as a matrix with lines
print("Win Rate Matrix (Rows: Model vs Columns: Model):")

# Print the header (column names) with lines between columns
print(f"{'':<15}|", end="")  # Add a separator line at the start
for model in model_names:
    print(f"{model:<15}|", end="")
print("\n" + "-" * (len(model_names) * 17 + 16))  # Add a separator line for the header

# Print the matrix with rows and lines between them
for i, model1 in enumerate(model_names):
    print(f"{model1:<15}|", end="")  # Add separator for the start of each row
    for j in range(len(model_names)):
        print(f"{win_rate_matrix[i, j]:<25}|", end="")  # Add separator between values
    print()  # Newline after each row
    print("-" * (len(model_names) * 17 + 16))  # Add separator line after each row
