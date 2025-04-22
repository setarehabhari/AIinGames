import os
import torch
import rlcard
from rlcard.agents.dmc_agent import DMCTrainer
import argparse

# ==== Fixed Parameters ====
CONFIG = {
    "env": "uno",  # Change to other game if needed
}

"""
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
    training_device=0,  # CUDA device ID or "cpu"
    savedir='experiments/uno_dmc_result/',
    total_frames=30000, #use at least 30 000, if below, it overrides it
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
    #print(args.total_frames)
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
        total_frames=args.total_frames,
    )

    # Start training
    trainer.start()

if __name__ == '__main__':
    train()
