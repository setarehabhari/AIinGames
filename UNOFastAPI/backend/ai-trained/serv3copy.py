from fastapi import FastAPI
from pydantic import BaseModel
from aimodule3 import *

# Initialize FastAPI app
app = FastAPI()

# Load AI agent and set up agents in the environment
ai_agent = load_ai_agent()
set_agents(ai_agent)


@app.get("/get_game_state")
def get_game_state_endpoint():
    """
    Returns the current state of the game for player 0.
    """
    return get_game_state()


@app.get("/get_legal_actions")
def get_legal_actions_endpoint():
    """
    Returns the legal actions available for the current player.
    """
    game_state = get_game_state()
    return game_state['legal_actions']


@app.get("/ai_legal_actions")
def ai_legal_actions():
    """
    Returns the AI's legal actions.
    """
    ai_actions = get_game_state()['legal_actions']
    return {"ai_legal_actions": ai_actions}

#
# @app.post("/play_card")
# async def play_card_endpoint(card_move: str):
#     """
#     Handle the human player's request to play a card.
#     """
#
#     result = human_move(card_move)
#     return result


# @app.post("/human_move")
# async def human_move_endpoint(card_move: str):
#     """
#     FastAPI endpoint for processing the human player's move.
#     """
#     result = human_move(card_move)
#     return result


# @app.post("/ai_move")
# async def ai_move_endpoint():
#     """
#     FastAPI endpoint for processing the AI's move.
#     """
#     result = ai_move()
#     return result
#

@app.post("/player_move")
async def play_card(card_move: str):
    """
    FastAPI endpoint for processing the AI's move.
    """
    # result = player_move(card_move)
    state_game = run(card_move)
    return state_game



@app.post("/suggestion")
async def suggest():
    """
    FastAPI endpoint for processing the AI's move.
    """
    # result = player_move(card_move)
    return suggestion()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
