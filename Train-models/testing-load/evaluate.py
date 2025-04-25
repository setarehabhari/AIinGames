''' An example of evluating the trained models in RLCard
'''
import os
import argparse
import random

import rlcard
from rlcard.agents import (
    DQNAgent,
    RandomAgent,
)
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    modifiedTournament,
)
import numpy

def load_model(model_path, env=None, position=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        torch.serialization.safe_globals([numpy.core.multiarray._reconstruct])
        torch.serialization.add_safe_globals([DQNAgent])
        agent = torch.load(model_path, map_location=device, weights_only=False)
        agent.set_device(device)
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    
    return agent

def evaluate(args):

    # Check whether gpu is available
    device = get_device()
        
    # Seed numpy, torch, random
    set_seed(args.seed)

    # Make the environment with seed
    env = rlcard.make('uno', config={'seed': args.seed})

    # Load models
    agents = []
    for position, model_path in enumerate(args.models):
        agents.append(load_model(model_path, env, position, device))
    env.set_agents(agents)

    # Evaluate
    # rewards = tournament(env, args.num_games)
    # for position, reward in enumerate(rewards):
    #     print(position, args.models[position], reward)

    avgRewards, allRewards = modifiedTournament(env, args.num_games)
    for position, reward in enumerate(avgRewards):
        print(position, args.models[position], reward)

    wins0 = allRewards[0].count(1)
    wins1 = allRewards[1].count(1)
    print(wins0)
    print(wins1)

    winRate0 = wins0/args.num_games
    winRate1 = wins1/args.num_games

    print(winRate0)
    print(winRate1)

    #each run to their own txt file
    model_names = f"{os.path.basename(args.models[0])}_vs_{os.path.basename(args.models[1])}".replace(" ", "_").replace(".", "_")
    log_filename = f"evaluation_5_{model_names}.txt"

    with open(log_filename, "w") as f:
        f.write(f"Number of Games: {args.num_games}\n")
        f.write(f"Models: {args.models}\n")
        for position, reward in enumerate(avgRewards):
            f.write(f"Player {position} ({args.models[position]}): Avg Reward = {reward}\n")
        f.write(f"Wins - Player 0: {wins0}, Player 1: {wins1}\n")
        f.write(f"Win Rate - Player 0: {winRate0}, Player 1: {winRate1}\n")
        f.write("="*40 + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Evaluation example in RLCard")
    parser.add_argument(
        '--models',
        nargs='*',
        default=[
            'random',
            'random',
        ],
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='0',
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=random.seed(None),
    )
    parser.add_argument(
        '--num_games',
        type=int,
        default=10000,
    )

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda
    evaluate(args)

