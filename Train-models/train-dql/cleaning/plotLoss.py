import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# Function to read RL-loss data from CSV files
def read_rl_losses_from_csv(file_path):
    steps = []
    rl_losses = []
    
    # Open the CSV file to read the steps and RL-loss values
    with open(file_path, 'r', encoding='utf-16') as loss_file:
        reader = csv.reader(loss_file)
        next(reader)  # Skip the header row
        for row in reader:
            step, rl_loss = row
            steps.append(int(step))
            rl_losses.append(float(rl_loss))
    
    return steps, rl_losses

# Path to the folder where RL-loss CSV files are saved
output_folder = "rl_losses"
output_plot_folder = "rl_plots"  # Folder where plots will be saved

# Create the output folder if it doesn't exist
if not os.path.exists(output_plot_folder):
    os.makedirs(output_plot_folder)

# Loop through all RL-loss CSV files in the folder and plot them
for filename in os.listdir(output_folder):
    if filename.endswith("_rl_losses.csv"):
        file_path = os.path.join(output_folder, filename)
        
        # Read the steps and RL-loss values from the CSV file
        steps, rl_losses = read_rl_losses_from_csv(file_path)
        
        # Convert to numpy arrays for easier manipulation
        steps_array = np.array(steps)
        rl_losses_array = np.array(rl_losses)

        # Normalize the steps and RL-losses by subtracting the mean and dividing by the standard deviation
        steps_mean = np.mean(steps_array)
        steps_std = np.std(steps_array)
        rl_losses_mean = np.mean(rl_losses_array)
        rl_losses_std = np.std(rl_losses_array)

        # Normalize the data
        normalized_steps = (steps_array - steps_mean) / steps_std
        normalized_rl_losses = (rl_losses_array - rl_losses_mean) / rl_losses_std

        # Perform linear regression on the normalized data
        m_normalized, b_normalized = np.polyfit(normalized_steps, normalized_rl_losses, 1)

        # Rescale the slope back to the original units
        m_scaled = m_normalized * (rl_losses_std / steps_std)
        b_scaled = rl_losses_mean - m_scaled * steps_mean
        
        # Create a new figure for the plot
        plt.figure(figsize=(10, 6))
        plt.ylim(0, 1.0)
        # Plot the RL-loss against steps
        plt.plot(steps_array, rl_losses_array, label=f"Session {filename.split('_')[1]}", linewidth=.5)

        # Plot the best fit line
        best_fit_line = m_scaled * steps_array + b_scaled
        plt.plot(steps_array, best_fit_line, label=f"Best Fit Line: y = {m_scaled:.5f}x + {b_scaled:.5f}", color='red', linestyle='--')

        # Add labels and a title to the plot
        plt.xlabel("Step")
        plt.ylabel("RL-loss")
        plt.title(f"RL-loss vs Step - {filename.split('_')[1]}")
        plt.legend()
        plt.grid(True)

        # Save the plot to a PNG file (without showing it)
        plot_filename = f"{filename.split('_')[1]}_rl_loss_plot.png"
        plot_path = os.path.join(output_plot_folder, plot_filename)
        plt.savefig(plot_path)  # Save the plot as PNG
        
        # Close the plot after saving it to free up memory
        plt.close()

        #print(f"Saved plot: {plot_filename}")
