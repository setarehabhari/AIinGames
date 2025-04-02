import rlcard
import torch
from rlcard.agents.human_agents.uno_human_agent import HumanAgent
# from rlcard.envs.uno import UnoEnv
from rlcard import models
import os
import argparse

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

env = rlcard.make('uno')
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# from backend.NewAIModule import suggest_move

global player_id, stt, trajectories, human_agent

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



def initialize_game():
    # Initialize the environment and agents
    # env.reset()
    global stt, player_id, trajectories, human_agent
    stt, player_id = env.reset()

    # Create the human agent
    human_agent = HumanAgent(env.num_actions)
    trajectories = [[] for _ in range(env.num_players)]



# Load the AI agent
def load_ai_agent():
    try:
        dqn_agent = load_model("model.pth", env, device=get_device())
        print("AI agent loaded successfully.")
        return dqn_agent
    except Exception as e:
        print(f"Error loading AI agent: {e}")
        return None


# Set the agents in the environment
def set_agents(ai_agent):
    try:
        env.set_agents([human_agent, ai_agent])
        print("Agents set in the environment successfully.")
    except Exception as e:
        print(f"Error setting agents in the environment: {e}")


# Get the current game state for player 0
def get_game_state(player_id=0):
    state_info = env.get_state(player_id)  # Get the state for player 0
    raw_state = state_info['raw_obs']

    game_state = {
        'hand': raw_state.get('hand', []),  # Player's hand
        'target': raw_state.get('target', None),  # Target card on the pile
        'played_cards': raw_state.get('played_cards', []),  # Cards played
        'legal_actions': raw_state.get('legal_actions', []),  # Legal actions available
        'num_cards': raw_state.get('num_cards', []),  # Number of cards per player
        'num_players': raw_state.get('num_players', 2),  # Number of players
        'current_player': raw_state.get('current_player', 0)  # Current player
    }
    return game_state


def run(action):
    # player_id = state['current_player']
    global trajectories
    global player_id
    state = get_game_state(player_id)

    trajectories[player_id].append(state)

    if not env.is_over():
        if player_id == 0:
            next_state, next_player_id = env.step(action, True)
        else:
            # next_state, next_player_id = env.step(action, env.agents[player_id].use_raw)
            ai_action = env.agents[1].step(env.get_state(1))  # Get AI's action (AI is player 1)
            next_state, next_player_id = env.step(ai_action)  # Apply the AI's action to the environment
            # state = get_game_state()  # Get the new game state

        trajectories[player_id].append(action)

        # Set the state and player
        # state = next_state
        player_id = next_player_id

        # Save state.
        # if not env.game.is_over():
        #     trajectories[player_id].append(state)
        # for pid in range(env.num_players):
        #     state = env.get_state(pid)
        #     trajectories[pid].append(state)
        #
        # # Payoffs
        payoffs = env.get_payoffs()
        state = get_game_state(player_id)
        return state


def suggestion():
    ai_suggestion = env.agents[1].step(env.get_state(0))
    # UnoEnv.decode_action_api(ai_suggestion)

    suggested_action = env.decode_action_api(ai_suggestion)
    return suggested_action
