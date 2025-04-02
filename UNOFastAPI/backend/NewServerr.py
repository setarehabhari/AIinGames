from fastapi import FastAPI
from pydantic import BaseModel
from NewAIModule import *

app = FastAPI()



@app.get("/get_game_state")
def get_game_state_endpoint():
    return get_game_state()


@app.get("/get_legal_actions")
def get_legal_actions_endpoint():
    return get_legal_actions()


# API Endpoint to get AI's legal actions
@app.get("/ai_legal_actions")
def ai_legal_actions():
    actions = get_ai_legal_actions()
    return {"ai_legal_actions": actions}

@app.post("/play_card")
async def play_card_endpoint(card: str):
    """
    Handle the request from the human player to play a card,
    process AI's move, and return the updated game state.
    """
    # card = request.card  # Get the card from the human player

    # Process the game logic using the play_card function from game.py
    result = play_card(card)

    return result


@app.post("/human_move")
async def human_move_endpoint(card: str):
    """
    FastAPI endpoint for processing the human player's move.
    """
    result = human_move(card)
    return result


@app.post("/ai_move")
async def ai_move_endpoint():
    """
    FastAPI endpoint for processing the AI's move.
    """
    result = ai_move()
    return result


@app.post("/human_draw")
async def human_draw():
    """
    FastAPI endpoint to allow the human to draw a card.
    """
    result = human_draw_card()
    return result


@app.get("/suggest-human-move")
async def get_suggestion_for_human():
    """
    API endpoint to get a suggestion for the human player's next move based on the DQN model.
    """
    suggestion = suggest_move()  # Get the suggestion for the human player
    return suggestion

@app.get("/turn")
async def show_turn_endpoint():
    """
    Endpoint to display whose turn it is, considering special card effects like Skip and Reverse.
    """
    turn_message = display_turn()
    return {"message": turn_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
