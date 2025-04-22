import os
import torch
import rlcard
from rlcard.agents.dmc_agent import DMCTrainer
import argparse
from datetime import datetime

# ==== Fixed Parameters ====
CONFIG = {
    "env": "uno",
}

# ==== Base Arguments ====
BASE_ARGS = {
    "is_pettingzoo_env": False,
    "load_model": False,
    "xpid": "dmc",
    "save_interval": 30,
    "num_actor_devices": 1,
    "num_actors": 5,
    "training_device": 0,
    "total_frames": 100000,
    "exp_epsilon": 0.01,
    "batch_size": 32,
    "unroll_length": 100,
    "num_buffers": 50,
    "num_threads": 4,
    "max_grad_norm": 40,
    "learning_rate": 0.0001,
    "alpha": 0.99,
    "momentum": 0,
    "epsilon": 0.00001,
}

def generate_savedir(training_device):
    # Get the current date and time
    now = datetime.now()
    day = now.strftime("%d")  # Day (two digits)
    hour = now.strftime("%H")  # Hour (two digits)
    minute = now.strftime("%M")  # Minute (two digits)
    # Use the training device index (e.g., "cuda:0", "cpu", etc.)
    device_str = str(training_device)
    
    # Construct the save directory name
    savedir = f"experiments/uno_dmc_grid_{day}_{hour}_{minute}_{device_str}/"
    os.makedirs(savedir, exist_ok=True)  # Ensure the directory exists
    return savedir

def train(args_dict, run_name):
    args = argparse.Namespace(**args_dict)
    args.xpid = run_name
    # Update savedir dynamically based on the current date and time
    args.savedir = generate_savedir(args.training_device)

    # Save args to txt file
    # args_log_path = os.path.join(args.savedir, "args.txt")
    # with open(args_log_path, "w") as f:
    #     for key, value in vars(args).items():
    #         f.write(f"{key}: {value}\n")

    env = rlcard.make(CONFIG["env"])

    trainer = DMCTrainer(
        env,
        cuda=args.training_device,
        load_model=args.load_model,
        xpid=args.xpid,
        savedir=args.savedir,
        save_interval=args.save_interval,
        num_actor_devices=args.num_actor_devices,
        num_actors=args.num_actors,
        training_device=args.training_device,
        total_frames=args.total_frames,
    )

    trainer.start()

def run_train_with_params(param_sets):
    for params in param_sets:
        train(params, params["run_name"])

# ==== Grid Search Settings ====
unroll_lengths = [25, 50, 75]

param_sets = []
for ul in unroll_lengths:
    args = BASE_ARGS.copy() 
    args["unroll_length"] = ul
    args["run_name"] = f"ul{ul}" 
    param_sets.append(args) 

if __name__ == '__main__':
    # Run baseline + grid search
    train(BASE_ARGS, "baseline")
    run_train_with_params(param_sets)
