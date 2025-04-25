import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to read hyperparameters from the log file and compare them
def extract_hyperparameters(log_path):
    hyperparameters = {}
    with open(log_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith('epsilon_start'):
                hyperparameters['epsilon_start'] = float(line.split(':')[1].strip())
            elif line.startswith('epsilon_end'):
                hyperparameters['epsilon_end'] = float(line.split(':')[1].strip())
            elif line.startswith('discount_factor'):
                hyperparameters['discount_factor'] = float(line.split(':')[1].strip())
            elif line.startswith('epsilon_decay_steps'):
                hyperparameters['epsilon_decay_steps'] = int(line.split(':')[1].strip())
    return hyperparameters

# Function to calculate slope (simple approximation)
def calculate_slope(df):
    rewards = df['reward'].values
    x = np.arange(len(rewards))  # Time steps (episodes)
    if len(rewards) > 1:
        slope = np.polyfit(x, rewards, 1)[0]  # Fit a line and get the slope
    else:
        slope = 0
    return slope

# Log file path
log_file_path = 'eval_dqn_params.txt'

# Directory with the run folders
base_dir = 'uno_dqn_result_GPU_test'

# Initialize data containers
hyperparameter_data = {
    'epsilon_start': {},
    'epsilon_end': {},
    'discount_factor': {},
    'epsilon_decay_steps': {}
}

# Collect data for each run
for run_dir in os.listdir(base_dir):
    if run_dir.startswith("run_"):
        run_path = os.path.join(base_dir, run_dir)
        run_id = run_dir.split('_')[-1]
        csv_path = os.path.join(run_path, f"performance_grid_search_{run_id}.csv")
        log_path = os.path.join(run_path, f"log_grid_search_{run_id}.txt")

        if os.path.exists(csv_path) and os.path.exists(log_path):
            # Read performance data
            df = pd.read_csv(csv_path)
            df.columns = df.columns.str.strip().str.lower()

            # Read hyperparameters from log file
            hyperparameters = extract_hyperparameters(log_path)

            # Calculate performance metrics
            avg_reward = df['reward'].mean()
            max_reward = df['reward'].max()
            slope = calculate_slope(df)

            # Add to hyperparameter data
            for param in hyperparameters:
                param_value = hyperparameters[param]
                if param_value not in hyperparameter_data[param]:
                    hyperparameter_data[param][param_value] = {'avg_reward': [], 'max_reward': [], 'slope': []}
                hyperparameter_data[param][param_value]['avg_reward'].append(avg_reward)
                hyperparameter_data[param][param_value]['max_reward'].append(max_reward)
                hyperparameter_data[param][param_value]['slope'].append(slope)

# Open the log file for writing
with open(log_file_path, 'w') as log_file:
    # Iterate over each hyperparameter
    for param, param_data in hyperparameter_data.items():
        log_file.write(f"=== {param} ===\n")
        
        # Initialize lists to store statistics for comparison
        avg_rewards_all_values = []
        max_rewards_all_values = []
        slopes_all_values = []

        for param_value, metrics in param_data.items():
            avg_reward = np.mean(metrics['avg_reward'])
            max_reward = np.mean(metrics['max_reward'])
            slope = np.mean(metrics['slope'])
            
            # Log individual hyperparameter results
            log_file.write(f"Hyperparameter: {param} = {param_value}\n")
            log_file.write(f"Average Reward: {avg_reward:.4f}\n")
            log_file.write(f"Max Reward: {max_reward:.4f}\n")
            log_file.write(f"Slope: {slope:.4f}\n\n")

            # Collect data for later comparison
            avg_rewards_all_values.append(avg_reward)
            max_rewards_all_values.append(max_reward)
            slopes_all_values.append(slope)

            # Visualize the effect of each hyperparameter on its own plot
            plt.figure(figsize=(10, 6))
            plt.plot(metrics['avg_reward'], label="Avg Reward", marker='o')
            plt.xlabel("Run")
            plt.ylabel("Avg Reward")
            plt.title(f"Effect of {param}={param_value} on Average Reward")
            plt.grid(True)

            # Set x and y axis ranges
            plt.xlim(0, len(metrics['avg_reward']) - 1)  # Dynamic x-axis based on the number of runs
            plt.xticks(np.arange(0, len(metrics['avg_reward']), 2))  # Ticks every 2 runs (adjust as needed)
            plt.ylim(-0.0001, 0.04)
            plt.yticks(np.arange(-0.01, 0.041, 0.005))

            # Save the individual plot
            plot_file_path = os.path.join(".", f"{param}_vs_avg_reward_{param_value}.png")
            plt.savefig(plot_file_path)
            plt.close()

        # Create a table-like summary for each hyperparameter
        log_file.write(f"Comparison of {param} Values:\n")
        for i, param_value in enumerate(param_data.keys()):
            log_file.write(f"{param}={param_value} | Avg Reward: {avg_rewards_all_values[i]:.4f}, Max Reward: {max_rewards_all_values[i]:.4f}, Slope: {slopes_all_values[i]:.4f}\n")

        log_file.write("\n" + "="*50 + "\n")

        # Now, create a combined plot for all values of this hyperparameter
        plt.figure(figsize=(10, 6))
        plt.xlabel("Run")
        plt.ylabel("Avg Reward")
        plt.title(f"Effect of {param} on Average Reward")
        
        # Plot each hyperparameter value on the same graph
        for i, (param_value, metrics) in enumerate(param_data.items()):
            avg_rewards = metrics['avg_reward']
            label = f"{param} = {param_value}"  # Label for the legend
            plt.plot(avg_rewards, label=label, marker='o', linestyle='-', color=plt.cm.viridis(i / len(param_data)))  # Using a color map to differentiate lines
        
        # Add grid, legend, and axis limits
        plt.grid(True)
        plt.xlim(0, len(avg_rewards) - 1)  # Dynamic x-axis based on the number of runs
        plt.xticks(np.arange(0, len(avg_rewards), 2))
        plt.ylim(-0.0001, 0.04)
        plt.yticks(np.arange(-0.01, 0.041, 0.005))

        # Add a legend to distinguish the lines
        plt.legend()

        # Save the combined plot with all values of the hyperparameter in the filename
        combined_plot_file_path = os.path.join(".", f"{param}_vs_avg_reward_all_values.png")
        plt.savefig(combined_plot_file_path)
        plt.close()

# Finished message
print("Evaluation complete. Results are logged to 'eval_dqn_params.txt' and plots are saved.")
