import os
import re
import statistics
import csv

base_dir = 'experiments/uno_dqn_result_4_22_1'
results = []

output_file_path = os.path.join(base_dir, 'grid_search_results.txt')

# Match folders like: eps0.2_gamma0.95_lr0.01_decay5000
folder_pattern = re.compile(r'^eps[\d.]+_gamma[\d.]+_lr[\d.]+_decay[\d.]+$')

for folder_name in os.listdir(base_dir):
    print(folder_name)
    if folder_pattern.match(folder_name):
        print("match")
        folder_path = os.path.join(base_dir, folder_name)
        log_filename = f'performance_{folder_name}.csv'
        print(log_filename)
        log_path = os.path.join(folder_path, log_filename)
        print(log_path)
        if not os.path.isfile(log_path):
            print(f"Log file not found: {log_path}")
            continue

        with open(log_path, 'r') as f:
            content = f.read()

        rewards = []
        with open(log_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    rewards.append(float(row['reward']))
                except (ValueError, KeyError):
                    continue
        print(rewards)

        if rewards:
            results.append({
                'run': folder_name,
                'max': max(rewards),
                'min': min(rewards),
                'mean': round(statistics.mean(rewards), 4)
            })

with open(output_file_path, 'w') as output_file:
    output_file.write(f"{'Run':<40} {'Max':<6} {'Min':<6} {'Mean':<6}\n")
    for r in sorted(results, key=lambda x: x['max'], reverse=True):
        output_file.write(f"{r['run']:<40} {r['max']:<6.2f} {r['min']:<6.2f} {r['mean']:<6.2f}\n")

print(f"Results have been written to {output_file_path}")
