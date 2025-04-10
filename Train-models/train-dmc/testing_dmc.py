import os
import torch
import rlcard
from rlcard.agents.dmc_agent import DMCTrainer
import argparse

# ==== Fixed Parameters ====
CONFIG = {
    "env": "uno",  # Change to other game if needed
}

# ==== Default Args as Namespace ====
# args = argparse.Namespace(
#     is_pettingzoo_env=False,
#     load_model=False,
#     xpid='dmc',
#     save_interval=30,
#     num_actor_devices=1,
#     num_actors=5,
#     training_device='',  # CUDA device ID or "cpu"
#     savedir='experiments/uno_dmc_result/',
#     total_frames=1_000_000,
#     exp_epsilon=0.01,
#     batch_size=32,
#     unroll_length=100,
#     num_buffers=50,
#     num_threads=4,
#     max_grad_norm=40,
#     learning_rate=0.0001,
#     alpha=0.99,
#     momentum=0,
#     epsilon=0.00001,
# )

args = argparse.Namespace(
    is_pettingzoo_env=False,
    load_model=False,
    xpid='dmc',
    save_interval=30,
    num_actor_devices=1,
    num_actors=5,
    training_device='',  # CUDA device ID or "cpu"
    savedir='experiments/uno_dmc_result/',
    total_frames=100000,
    exp_epsilon=0.01,
    batch_size=8,
    unroll_length=25,
    num_buffers=10,
    num_threads=2,
    max_grad_norm=40,
    learning_rate=0.0001,
    alpha=0.99,
    momentum=0,
    epsilon=0.00001,
)

def train():
    # Make the environment
    env = rlcard.make(CONFIG["env"])

    # Initialize the DMC trainer
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
    )

    # Start training
    trainer.start()

if __name__ == '__main__':
    train()
