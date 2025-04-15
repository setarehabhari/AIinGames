import os
import re
import argparse

# Initialize variables
current_session = {"parameters": [], "episodes": []}
current_rl_losses = []
session_count = 0
sessions_info = []
param_pattern = re.compile(r"Testing with parameters:", re.IGNORECASE)
config_pattern = re.compile(r"^=========CONFIG=========", re.IGNORECASE)
args_pattern = re.compile(r"^==========ARGS=========", re.IGNORECASE)
loss_pattern = re.compile(r"INFO - Step (\d+), rl-loss: ([0-9\.]+)", re.IGNORECASE)

# Path to save parameters and RL-losses
output_folder = "rl_losses"
os.makedirs(output_folder, exist_ok=True)

# Function to save parameters to a file
def save_session_parameters(parameters, session_number):
    filename = os.path.join(output_folder, f"session_{session_number}_parameters.txt")
    with open(filename, "w", encoding="utf-16") as param_file:
        for param in parameters:
            param_file.write(param + "\n")

# Function to save RL losses to CSV
def save_rl_losses_to_csv(rl_losses, session_number):
    filename = os.path.join(output_folder, f"session_{session_number}_rl_losses.csv")
    with open(filename, "w", encoding="utf-16") as loss_file:
        loss_file.write("step,rl_loss\n")
        for step, rl_loss in enumerate(rl_losses, start=1):
            loss_file.write(f"{step},{rl_loss}\n")

# Function to save session info
def save_session_info(sessions_info):
    with open(os.path.join(output_folder, "session_info.txt"), "w", encoding="utf-16") as info_file:
        for session in sessions_info:
            info_file.write(session + "\n")
    print("Saved session information.")

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Process a log file to extract RL losses and parameters.")
parser.add_argument("log_file", help="Path to the log file to process")
args = parser.parse_args()

# Simulating reading the log file line by line
with open(args.log_file, 'r', encoding='utf-16') as file:
    capturing_config = False
    capturing_args = False
    for line in file:
        # Detect the start of a parameter block
        if param_pattern.search(line):
            
            # If we already have a session, save the previous session's data
            if current_session["parameters"]:
                save_rl_losses_to_csv(current_rl_losses, session_count)
                save_session_parameters(current_session["parameters"], session_count)
            
            # Reset for the new session
            current_session = {"parameters": [], "episodes": []}
            current_rl_losses = []
            session_count += 1
            
            # Add the first parameter line for this session
            current_session["parameters"].append(line.strip())

        # Handle CONFIG section
        elif config_pattern.search(line):
            capturing_config = True
            capturing_args = False  # Stop capturing ARGs section
            current_session["parameters"].append(line.strip())  # Save the config header line
        
        # Handle ARGS section
        elif args_pattern.search(line):
            capturing_args = True
            capturing_config = False  # Stop capturing CONFIG section
            current_session["parameters"].append(line.strip())  # Save the args header line

        # Capture configuration/arguments lines (only during CONFIG/ARGS sections)
        elif capturing_config or capturing_args:
            current_session["parameters"].append(line.strip())

        # Detect RL-loss lines and store them in the rl_losses list
        elif loss_pattern.match(line):
            match = loss_pattern.match(line)
            if match:
                rl_loss = float(match.group(2))  # Extract the rl-loss value
                current_rl_losses.append(rl_loss)

# After finishing reading the file, make sure to save the last session's data
if current_session["parameters"]:
    save_rl_losses_to_csv(current_rl_losses, session_count)
    save_session_parameters(current_session["parameters"], session_count)

# Optionally save the session information (parameter summary)
save_session_info(sessions_info)
