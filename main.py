# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from game_engine import LoveLetterGameEngine

app = FastAPI()

# In-memory storage for now
users = {}  # username -> password hash
games = {}  # game_id -> LoveLetterGameEngine instance
game_counter = 1

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateGameRequest(BaseModel):
    player_names: list[str]

class PlayCardRequest(BaseModel):
    player_name: str
    card_index: int
    target_name: str = None
    guess: str = None

@app.post("/register")
def register(req: RegisterRequest):
    if req.username in users:
        raise HTTPException(status_code=400, detail="User exists")
    users[req.username] = req.password  # TODO: hash passwords
    return {"message": "Registered successfully"}

@app.post("/login")
def login(req: LoginRequest):
    if req.username not in users or users[req.username] != req.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.post("/game/create")
def create_game(req: CreateGameRequest):
    global game_counter
    game_id = game_counter
    game_counter += 1
    engine = LoveLetterGameEngine(req.player_names)
    engine.start_round()
    games[game_id] = engine
    return {"game_id": game_id, "state": engine.get_game_state()}

@app.get("/game/{game_id}/state")
def get_game_state(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id].get_game_state()

@app.post("/game/{game_id}/play")
def play_card(game_id: int, req: PlayCardRequest):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id].play_card(req.player_name, req.card_index, req.target_name, req.guess)
