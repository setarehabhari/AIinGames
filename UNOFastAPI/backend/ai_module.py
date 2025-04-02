import rlcard as rlcard
import numpy as np
#
env = rlcard.make('uno')
# state, _ = env.reset()


#TODO suggestions
# Give the AI played card
# draw card
def initialize_game():
    env.reset()  # Resets the environment and starts a new game.
    return "Game Initialized"

def get_game_state():
    state_info = env.get_state(0)  # Get the state for player 0
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

def get_legal_actions():
    state_info = env.get_state(0)  # Get state for the player
    legal_actions = state_info['raw_obs']['legal_actions']
    return legal_actions


def play_card(player_id, card):
    state_info = env.get_state(player_id)  # Get state for the player
    legal_actions = state_info['raw_obs']['legal_actions']

    if card in legal_actions:
        env.step(card, True)  # Make the move with the chosen card
        return get_game_state()  # Return updated state
    else:
        return {"error": "Invalid card"}
