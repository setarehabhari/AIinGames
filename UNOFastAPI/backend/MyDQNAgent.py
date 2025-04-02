import os
import argparse

import rlcard
from rlcard.agents import (
    DQNAgent,
    RandomAgent,
)
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)
import numpy


def load_model(model_path, env=None, position=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        torch.serialization.safe_globals([numpy.core.multiarray._reconstruct])
        torch.serialization.add_safe_globals([DQNAgent])
        agent = torch.load(model_path, map_location=device, weights_only=False)
        agent.set_device(device)
    # elif os.path.isdir(model_path):  # CFR model
    #     from rlcard.agents import CFRAgent
    #     agent = CFRAgent(env, model_path)
    #     agent.load()
    # elif model_path == 'random':  # Random model
    #     from rlcard.agents import RandomAgent
    #     agent = RandomAgent(num_actions=env.num_actions)
    # else:  # A model in the model zoo
    #     from rlcard import models
    #     agent = models.load(model_path).agents[position]

    return agent