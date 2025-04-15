import os
import re

# Initialize variables
current_session = {"parameters": [], "episodes": []}
current_rl_losses = []
session_count = 0
sessions_info = []
param_pattern = re.compile(r"Testing with parameters:", re.IGNORECASE)

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

# Simulating reading the log file line by line
with open('./4-9-21h41m.log', 'r', encoding='utf-16') as file:
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
        
        # If this line is part of the config or parameters section (in "CONFIG" and "ARGS" sections), add to parameters
        elif "epsilon_start" in line or "epsilon_end" in line or "batch_size" in line or "learning_rate" in line or \
             "discount_factor" in line or "mlp_layers" in line or "epsilon_decay_steps" in line or \
             "replay_memory_size" in line or "num_episodes" in line or "num_eval_games" in line:
            current_session["parameters"].append(line.strip())
        
        # Detect RL-loss lines and store them in the rl_losses list
        elif "INFO - Step" in line and "rl-loss" in line:
            parts = line.split("rl-loss:")
            if len(parts) > 1:
                rl_loss = parts[1].strip()
                current_rl_losses.append(float(rl_loss))
        
        # Detect episode and reward data (if needed for later)
        elif "episode" in line and "reward" in line:
            # Store episode info if needed (optional)
            pass

# After finishing reading the file, make sure to save the last session's data
if current_session["parameters"]:
    save_rl_losses_to_csv(current_rl_losses, session_count)
    save_session_parameters(current_session["parameters"], session_count)

# Optionally save the session information (parameter summary)
save_session_info(sessions_info)
