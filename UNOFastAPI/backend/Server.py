# backend/server.py
from fastapi import FastAPI
from backend.ai_module import get_legal_actions, get_game_state, play_card, initialize_game

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the UNO game!"}

@app.get("/start_game")
def start_game():
    return initialize_game()

@app.get("/get_game_state")
def get_game_state_endpoint():
    return get_game_state()


@app.get("/get_legal_actions")
def get_legal_actions_endpoint():
    return get_legal_actions()

@app.post("/play_card")
def play_card_endpoint(card: str):
    # Assuming you pass the card and player ID in the body or URL
        return play_card(0, card)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
