import os
import torch
import rlcard
from rlcard.agents.dmc_agent import DMCTrainer
import argparse

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
    "training_device":'',
    "savedir": "experiments/uno_dmc_grid_4_22_5CPU/",
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

def train(args_dict, run_name):
    args = argparse.Namespace(**args_dict)
    args.xpid = run_name
    #args.savedir = os.path.join(BASE_ARGS["savedir"], run_name)
    #os.makedirs(args.savedir, exist_ok=True)

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

    """
    Deep Monte-Carlo

    Args:
        env: RLCard environment
        load_model (boolean): Whether loading an existing model
        xpid (string): Experiment id (default: dmc)
        save_interval (int): Time interval (in minutes) at which to save the model
        num_actor_devices (int): The number devices used for simulation
        num_actors (int): Number of actors for each simulation device
        training_device (str): The index of the GPU used for training models, or `cpu`.
        savedir (string): Root dir where experiment data will be saved
        total_frames (int): Total environment frames to train for
        exp_epsilon (float): The prbability for exploration
        batch_size (int): Learner batch size
        unroll_length (int): The unroll length (time dimension)
        num_buffers (int): Number of shared-memory buffers
        num_threads (int): Number learner threads
        max_grad_norm (int): Max norm of gradients
        learning_rate (float): Learning rate
        alpha (float): RMSProp smoothing constant
        momentum (float): RMSProp momentum
        epsilon (float): RMSProp epsilon
    """


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
