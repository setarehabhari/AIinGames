import os
import torch
import rlcard
from rlcard.agents.dmc_agent import DMCTrainer
import argparse
from datetime import datetime
from itertools import product

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
    "training_device": '',
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

# Generate main save directory once
def generate_base_savedir(training_device):
    now = datetime.now()
    timestamp = now.strftime("%d_%H_%M")
    device_str = str(training_device)
    savedir = f"experiments/uno_dmc_grid_{timestamp}_{device_str}/"
    os.makedirs(savedir, exist_ok=True)
    return savedir

BASE_SAVE_DIR = generate_base_savedir(BASE_ARGS["training_device"])
BASE_ARGS["savedir"] = BASE_SAVE_DIR

def train(args_dict, run_name):
    args = argparse.Namespace(**args_dict)
    args.xpid = run_name
    args.savedir = os.path.join(BASE_SAVE_DIR, run_name)
    os.makedirs(args.savedir, exist_ok=True)

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
batch_sizes = [32, 64, 128]
learning_rates = [1e-4, 5e-4, 1e-3]
exp_epsilons = [0.01, 0.05, 0.1]

param_sets = []
for ul, bs, lr, eps in product(unroll_lengths, batch_sizes, learning_rates, exp_epsilons):
    args = BASE_ARGS.copy()
    args["unroll_length"] = ul
    args["batch_size"] = bs
    args["learning_rate"] = lr
    args["exp_epsilon"] = eps
    args["run_name"] = f"ul{ul}_bs{bs}_lr{lr}_eps{eps}"
    param_sets.append(args)

if __name__ == '__main__':
    train(BASE_ARGS, "baseline")
    run_train_with_params(param_sets)
