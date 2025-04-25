import os
import re
import numpy as np

# calculates the overall win rates of each model
model_win_rates = {}

# Adjust this path to where your result files are stored
folder_path = "./"

# Read each result file
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), "r") as f:
            lines = f.readlines()
            for line in lines:
                match = re.match(r"Win Rate - Player 0: ([0-9.]+), Player 1: ([0-9.]+)", line)
                if match:
                    rate0, rate1 = float(match[1]), float(match[2])
                    model0 = re.search(r"Models: \['([^']+)", lines[1])[1]
                    model1 = re.search(r", '([^']+)'\]", lines[1])[1]

                    model_win_rates.setdefault(model0, []).append(rate0)
                    model_win_rates.setdefault(model1, []).append(rate1)

# Print summary
for model, rates in model_win_rates.items():
    avg = np.mean(rates)
    std = np.std(rates)
    print(f"{model}: Avg Win Rate = {avg:.4f}, Std Dev = {std:.4f}")
