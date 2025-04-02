import rlcard as rlcard
from rlcard import models
from rlcard.agents.human_agents.uno_human_agent import HumanAgent

trajectories = []

# Initialize the environment
env = rlcard.make('uno')

# Reset the environment (very important)
env.reset()

# Create the human agent
human_agent = HumanAgent(env.num_actions)  # Human agent
# print("Human agent created with actions:", env.num_actions)

# Load the AI agent
try:
    cfr_agent = models.load('uno-rule-v1').agents[0]  # AI agent
    print("AI agent loaded successfully.")
except Exception as e:
    print(f"Error loading AI agent: {e}")

# Set the agents in the environment
try:
    env.set_agents([human_agent, cfr_agent])  # Set agents in the environment
    print("Agents set in the environment successfully.")
except Exception as e:
    print(f"Error setting agents in the environment: {e}")



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


# def get_game_state():
#     # Get the game state, including the player's hand and other relevant info
#     state_info = env.get_state(0)
#     print(state_info)
#     raw_state = state_info['raw_obs']
#
#     game_state = {
#         'hand': raw_state.get('hand', []),  # Player's hand
#         'target': raw_state.get('target', None),  # Target card on the pile
#         'played_cards': raw_state.get('played_cards', []),  # Cards played
#         'num_cards': raw_state.get('num_cards', []),  # Number of cards per player
#         'num_players': raw_state.get('num_players', 2),  # Number of players
#
#     }
#     return game_state

# def play_card(card):
#     """
#     Process the human's card choice, play the AI's turn, and return the updated game state or result.
#     """
#     state_info = env.get_state(0)  # Get state for human player
#     legal_actions = state_info['raw_obs']['legal_actions']
#
#     # Check if the chosen card is valid
#     if card not in legal_actions:
#         return {"error": "Invalid card"}
#
#     # Human plays the card
#     env.step(card, True)
#
#     # Now it's AI's turn to play
#     if not env.is_over():
#         ai_state = env.get_state(1)
#         ai_action = cfr_agent.step(ai_state)
#         env.step(ai_action, True)
#
#     # Check if the game is over and get the result
#     if env.is_over():
#         payoffs = env.get_payoffs()
#         result = {
#             "game_over": True,
#             "payoffs": payoffs,
#             "message": "Game Over",
#             "winner": "AI" if payoffs[1] > 0 else "Human"
#         }
#     else:
#         # If the game is not over, return the updated state
#         updated_state = get_game_state()
#         result = {"game_over": False, "state": updated_state}
#
#     return result




def human_move(card):
    """
    Process the human player's card choice and return the updated game state or error if the card is invalid.
    """
    state_info = env.get_state(0)  # Get state for human player
    legal_actions = state_info['raw_obs']['legal_actions']

    # Check if the chosen card is valid
    if card not in legal_actions:
        return {"error": "Invalid card"}

    # Human plays the card
    env.step(card, True)

    # Get updated state after the human's move
    updated_state = get_game_state()
    return updated_state

    # return {"game_over": False, "state": updated_state}

#
# def ai_move():
#     """
#     Process the AI's move and return the updated game state.
#     """
#     if env.is_over():  # Check if the game is already over
#         return {"game_over": True, "message": "Game Over"}
#
#     ai_state = env.get_state(1)  # Get the state for the AI player
#     legal_actions = ai_state['raw_obs']['legal_actions']
#     print("Legal actions available to AI:", legal_actions)
#     ai_action = cfr_agent.step(ai_state)
#     print("AI selected action:", ai_action)
#     if ai_action not in legal_actions:
#         print("Invalid AI action!")
#
#     # Now it's AI's turn to play
#     ai_state = env.get_state(1)
#     ai_action = cfr_agent.step(ai_state, True )
#     env.step(ai_action, True)
#
#     # Get updated state after the AI's move
#     updated_state = get_game_state()
#
#     return {"game_over": False, "state": updated_state}


def track_action(player_id, action):
    state_info = env.get_state(player_id)
    trajectories.append({
        'player_id': player_id,
        'state': state_info['raw_obs'],
        'action': action
    })

def check_game_result():
    if env.is_over():
        payoffs = env.get_payoffs()
        print("Game Over! Payoffs:", payoffs)
        return {"game_over": True, "payoffs": payoffs}
    else:
        print("Game is not over yet.")
        return {"game_over": False}

# def human_move(card):
#     state_info = env.get_state(0)
#     legal_actions = state_info['raw_obs']['legal_actions']
#
#     if card not in legal_actions:
#         return {"error": "Invalid card"}
#
#     env.step(card, True)
#     track_action(0, card)
#
#     return check_game_result() or {"game_over": False, "state": get_game_state()}

#
# def ai_move():
#     if env.is_over():
#         return check_game_result()
#
#     ai_state = env.get_state(1)
#     legal_actions = ai_state['raw_obs']['legal_actions']
#
#     ai_action = cfr_agent.step(ai_state)
#
#     # Ensure AI action is valid
#     if ai_action not in legal_actions:
#         print(f"Invalid AI action: {ai_action}")
#         return {"error": "AI selected an invalid action."}
#
#     # Handle special actions (wild cards and draws)
#     action_name = env._decode_action(ai_action)
#     if 'wild' in action_name:
#         declared_color = max(['r', 'g', 'b', 'y'], key=lambda c: ai_state['raw_obs']['hand'].count(f'{c}-'))
#         print(f"AI declared color: {declared_color}")
#         env.step((ai_action, declared_color), True)
#     elif 'draw' in action_name:
#         print("AI drew a card.")
#         env.step(ai_action, True)
#     else:
#         env.step(ai_action, True)
#
#     track_action(1, ai_action)
#     print("AI played:", action_name)
#
#     return check_game_result() or {"game_over": False, "state": get_game_state()}
#
#
ACTION_LIST = {
    0: "play_0",
    1: "play_1",
    2: "skip",
    3: "reverse",
    4: "wild",
    5: "wild_draw_4",
    6: "draw_2",
    # Add other actions here as needed
}




def ai_move():
    # Check if the game is over before making a move
    if env.is_over():
        return check_game_result()

    # Get the AI's state
    ai_state = env.get_state(1)
    legal_actions = ai_state['raw_obs']['legal_actions']

    # AI makes a move using the CFR agent
    ai_action = cfr_agent.step(ai_state)

    # Ensure AI action is valid
    if ai_action not in legal_actions:
        print(f"Invalid AI action: {ai_action}")
        return {"error": "AI selected an invalid action."}

    # Handle special actions (wild cards, skips, and draws)
    action_name = ACTION_LIST.get(ai_action, "Unknown Action")  # Look up the action from ACTION_LIST

    if 'wild' in action_name:
        # Handle wild card actions
        declared_color = max(['r', 'g', 'b', 'y'], key=lambda c: ai_state['raw_obs']['hand'].count(f'{c}-'))
        print(f"AI declared color: {declared_color}")
        env.step((ai_action, declared_color), True)
    elif 'draw' in action_name:
        # Handle draw actions
        print("AI drew a card.")
        env.step(ai_action, True)
    else:
        # Handle regular actions
        env.step(ai_action, True)

    # Track the action taken
    track_action(1, ai_action)
    print("AI played:", action_name)

    # Return the game result after the AI's move
    game_result = check_game_result()
    return get_game_state()
    # if game_result:
    #     return game_result
    # else:
    #     return {"game_over": False, "state": get_game_state()}




def play_card(card):
    """
    Process the human's card choice, then process the AI's move, and return the updated game state or result.
    """
    # Process the human player's move
    human_result = human_move(card)
    if "error" in human_result:  # If there's an error with the human's move, return the error
        return human_result

    # Now it's AI's turn to move
    ai_result = ai_move()

    return ai_result


def get_legal_actions():
    state_info = env.get_state(0)  # Get state for the player
    legal_actions = state_info['raw_obs']['legal_actions']
    return legal_actions



def ai_draw_card():
    """
    Simulate AI drawing a card when it has no legal actions.
    """
    # AI draws a card from the deck
    state_info = env.get_state(1)  # Get the state for the AI player (player_id = 1)
    legal_actions = state_info['raw_obs']['legal_actions']

    if not legal_actions:  # If AI has no legal actions, it must draw a card
        # Draw a card from the deck (simulating the draw by taking an action)
        action = 'draw'  # Assuming 'draw' is the action for drawing a card in the environment

        # Perform the draw action
        env.step(action, True)

        return {"message": "AI drew a card", "state": get_game_state()}

    return {"message": "AI can play a card", "state": get_game_state()}


def human_draw_card():
    """
    Allow the human player to draw a card from the deck.
    """
    # Get the current game state for the human player
    state_info = env.get_state(0)  # Get state for human player (player_id = 0)
    legal_actions = state_info['raw_obs']['legal_actions']

    # If human cannot play any card, they need to draw one
    if 'draw' in legal_actions:
        # Perform the draw action
        env.step('draw', True)  # Assuming 'draw' is the action for drawing a card in the environment

        # Get updated state after the draw
        updated_state = get_game_state()

        return {"message": "Human drew a card", "state": updated_state}

    return {"error": "Invalid action. Human can play a card or draw."}




from rlcard import models


# Load the rule-based agent ('uno-rule-v1') from rlcard models
dqn_agent = models.load('uno-rule-v1')

# Set up the agents: human player and rule-based AI agent
human_agent = HumanAgent(env.num_actions)  # Human agent (assuming you have already defined the HumanAgent)
env.set_agents([human_agent, dqn_agent])  # Set both agents in the environment


# Example: Get a suggestion for the human player (based on rule-based AI)
def suggest_move():
    """
    Suggests a move for the human player based on the AI's current state and the game model.
    Returns a suggested action (card to play).
    """
    # Get the current game state for the human player
    state_info = env.get_state(0)  # Get state for human player

    # Get the legal actions available to the human player (cards they can play)
    legal_actions = state_info['raw_obs']['legal_actions']

    if not legal_actions:
        return {"error": "No legal actions available"}

    # Here, we ask the rule-based AI to suggest a move for the human (it will choose a legal action)
    suggested_action = legal_actions[0]  # For simplicity, we're suggesting the first legal action

    return {"suggested_action": suggested_action}



# Function to get the legal actions for the AI
def get_ai_legal_actions():
    state_info = env.get_state(1)  # AI is the second player (player_id = 1)
    legal_actions = state_info['raw_obs']['legal_actions']
    return legal_actions


def display_turn():
    """
    Get the turn message considering the current player and the effects of special cards (Skip, Reverse).
    """
    last_played_card = env.get_state(0)['raw_obs']['played_cards'][-1] if len(env.get_state(0)['raw_obs']['played_cards']) > 0 else None
    direction = env.get_state(0)['raw_obs'].get('direction', 1)  # 1 is clockwise, -1 is counter-clockwise
    current_player = env.get_state(0)['raw_obs']['current_player']

    # Handle special cards (Skip and Reverse)
    if last_played_card:
        if "skip" in last_played_card:
            return "The next player is skipped!"
        if "reverse" in last_played_card:
            direction = -direction  # Reverse the direction
            return "The direction of play is reversed!"

    # Show whose turn it is based on the current player and direction
    if direction == 1:
        if current_player == 0:
            return "It's your turn!"
        else:
            return "It's AI's turn!"
    else:  # Counter-clockwise play
        if current_player == 1:
            return "It's your turn!"
        else:
            return "It's AI's turn!"