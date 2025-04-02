from fastapi import FastAPI
from pydantic import BaseModel
from aimodule3 import *

# Initialize FastAPI app
app = FastAPI()

# Load AI agent and set up agents in the environment
ai_agent = load_ai_agent()
set_agents(ai_agent)


@app.get("/get_human_game_state")
def get_human_game_state_endpoint():
    """
    Returns the current state of the game for player 0.
    """
    return get_game_state()



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
