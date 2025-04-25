import os
import pandas as pd

base_dir = 'uno_dqn_result_GPU_test'
results = []

# Function to calculate slope between consecutive episodes
def calculate_slope(df):
    # Calculate the change in reward and episode
    df['reward'] = df['reward'].astype(float)  # Ensure reward is float
    df['episode'] = df['episode'].astype(int)  # Ensure episode is integer
    df['slope'] = df['reward'].diff() / df['episode'].diff()  # Calculate slope as change in reward / change in episode
    return df['slope'].mean()  # Use mean slope for the entire run

for run_dir in os.listdir(base_dir):
    if run_dir.startswith("run_"):
        run_path = os.path.join(base_dir, run_dir)
        run_id = run_dir.split('_')[-1]
        csv_path = os.path.join(run_path, f"performance_grid_search_{run_id}.csv")
        
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)

                # Normalize column names
                df.columns = df.columns.str.strip().str.lower()

                if 'reward' in df.columns and 'episode' in df.columns:
                    # Calculate the slope for this run
                    slope = calculate_slope(df)
                    avg_reward = df['reward'].mean()  # Calculate the average reward for the run
                    max_reward = df['reward'].max()  # Get the max reward for the run
                    results.append((run_id, slope, avg_reward, max_reward))
            except Exception as e:
                continue  # Skip the run if any error occurs

# Sort runs by average reward in descending order
results.sort(key=lambda x: x[2], reverse=True)

# Write summary to text file
eval_file_path = os.path.join(base_dir, "eval_dqn_runs.txt")
with open(eval_file_path, "w") as f:
    if results:
        # Find the run with the highest slope
        best_slope = max(results, key=lambda x: x[1])
        # Find the run with the highest average reward
        best_avg_reward = max(results, key=lambda x: x[2])
        # Find the run with the highest reward
        best_max_reward = max(results, key=lambda x: x[3])
        
        for run_id, slope, avg_reward, max_reward in results:
            # Scale the slope value for better readability (optional)
            scaled_slope = slope * 1000  # Scale slope by 1000 to avoid small values like 0.000
            f.write(f"Run {run_id}: Avg Reward = {avg_reward:.5f}, Max Reward = {max_reward:.3f}, Slope = {scaled_slope:.5f}\n")
        
        f.write(f"\nBest Slope: Run {best_slope[0]} with Avg Reward = {best_slope[2]:.5f}, Slope = {best_slope[1] * 1000:.5f}\n")
        f.write(f"Best Avg Reward: Run {best_avg_reward[0]} with Avg Reward = {best_avg_reward[2]:.3f}, Slope = {best_avg_reward[1] * 1000:.5f}\n")
        f.write(f"Best Max Reward: Run {best_max_reward[0]} with Max Reward = {best_max_reward[3]:.3f}, Slope = {best_max_reward[1] * 1000:.5f}\n")
    else:
        f.write("No valid runs with 'reward' or 'episode' columns found.\n")

print(f"Results written to {eval_file_path}")
