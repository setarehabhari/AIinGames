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
    "training_device": 0,
    "total_frames": 100000,
    "exp_epsilon": 0.05,
    "batch_size": 32,
    "unroll_length": 25,
    "num_buffers": 50,
    "num_threads": 4,
    "max_grad_norm": 40,
    "learning_rate": 0.0001,
    "alpha": 0.99,
    "momentum": 0,
    "epsilon": 0.00001,
    "savedir": "./experiments"
}

def train(args_dict, run_name):
    args = argparse.Namespace(**args_dict)
    args.xpid = run_name

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

if __name__ == '__main__':
    train(BASE_ARGS, "DMC3")
    