import os
import re
import statistics

# Define the base directory where the run folders are located
base_dir = 'experiments/uno_dqn_result'  # This is the folder containing 'run_*' folders
results = []

# Define the output file path outside of the 'run_*' folders
output_file_path = os.path.join(base_dir, 'grid_search_results.txt')

# Iterate through run folders
for folder_name in os.listdir(base_dir):
    if folder_name.startswith('run_'):
        run_index = folder_name[4:]  # Get the number after "run"
        
        # Construct the log file path using os.path.join
        log_path = os.path.join(base_dir, folder_name, f'log_grid_search_{run_index}.txt')
        
        # Check if the log file exists
        if not os.path.isfile(log_path):
            print(f"Log file not found: {log_path}")
            continue
        
        # Read the content of the log file
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Extract reward values using regex
        rewards = [float(m.group(1)) for m in re.finditer(r'reward\s+\|\s+(-?\d+\.\d+)', content)]
        
        if rewards:
            result = {
                'run': run_index,
                'max': max(rewards),
                'min': min(rewards),
                'mean': round(statistics.mean(rewards), 4)
            }
            results.append(result)

# Write the results to the output text file outside the run folders
with open(output_file_path, 'w') as output_file:
    # Write header
    output_file.write(f"{'Run':<6} {'Max':<6} {'Min':<6} {'Mean':<6}\n")
    
 # Sort the results by 'max' value and then write the results
    for r in sorted(results, key=lambda x: x['max'], reverse=True):  # Sorting by 'max' in descending order
        output_file.write(f"{r['run']:<6} {r['max']:<6.2f} {r['min']:<6.2f} {r['mean']:<6.2f}\n")


print(f"Results have been written to {output_file_path}")
