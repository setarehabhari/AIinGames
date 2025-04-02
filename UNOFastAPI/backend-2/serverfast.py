from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aimodule import UNOGame  # Import the UNOGame class

# Initialize the FastAPI app and UNO game module
app = FastAPI()

# Create an instance of UNOGame class
game = UNOGame()

# Pydantic model for incoming request body
class ActionRequest(BaseModel):
    human_card: str  # The card the human player chooses to play
    human_hand: list  # The cards in the human player's hand
    ai_hand: list     # The cards in the AI player's hand

@app.post("/play")
async def play_turn(request: ActionRequest):
    try:
        # Get the data from the request
        human_card = request.human_card
        human_hand = request.human_hand
        ai_hand = request.ai_hand

        # Call the UNOGame play_turn method to process the game turn
        result = game.play_turn(human_card, human_hand, ai_hand)

        # Return the result to the client
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "UNO API is running! Send POST requests to /play to play the game."}


@app.get("/state")
async def get_state():
    return game.get_state()

@app.get("/legal_actions")
async def get_legal_actions():
    return game.get_legal_actions()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
