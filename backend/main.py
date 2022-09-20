"""
API endpoint definitions
"""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.models import GameModel
from backend.slot_machine import SlotMachine

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

SECRET = "slotmachine"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: also return symbols from this endpoint
@app.post("/play/", response_model=GameModel)
def play(request: Request, game_model: GameModel):
    if request.session.get(SECRET) is None:
        request.session[SECRET] = game_model.credit
    credit = request.session.get(SECRET)
    slot_machine = SlotMachine(credit=credit)
    slot_machine.play()
    request.session[SECRET] = slot_machine.credit
    return {"credit": slot_machine.credit}


@app.get("/cash_out/", response_model=GameModel)
def cash_out(request: Request):
    credit = request.session.get(SECRET)
    request.session[SECRET] = None
    return {"credit": credit}


# TODO: delete after testing
@app.get("/dummy/")
def dummy_endpoint():
    return {"roll": ["cherry", "lemon", "orange"]}
