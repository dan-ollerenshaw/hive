"""
API endpoint definitions
"""

import logging
import random

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from backend.exceptions import MissingSessionIDException, UnknownSessionIDException
from backend.models import CashOutResponseModel, PlayResponseModel, RequestModel
from backend.slot_machine import DEFAULT_CREDIT, SlotMachine

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FIXME: keeping track of sessions like this is bad
# but I had trouble retaining sessions info from the frontend
SESSION_ID_KEY = "x-session-id"
SESSIONS = {}

app = FastAPI()
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.post("/play/", response_model=PlayResponseModel)
def play(request: Request, request_model: RequestModel):
    session = get_session_from_request(request)
    credit = session["session_credit"] + request_model.account_credit
    slot_machine = SlotMachine(credit=credit)
    roll = slot_machine.play()
    session["session_credit"] = slot_machine.credit
    return {"session_credit": slot_machine.credit, "roll": roll}


@app.get("/cash_out/", response_model=CashOutResponseModel)
def cash_out(request: Request):
    session = get_session_from_request(request)
    credit = session["session_credit"]
    # reset the credit for this session
    session["session_credit"] = 0
    return {"account_credit": credit}


@app.get("/session_id/")
def create_session_id(request: Request, response: Response):
    # create a psuedo-random session ID
    session_id = f"{request.headers['user-agent']}_{random.randint(1,10**7)}"
    response.headers[SESSION_ID_KEY] = session_id
    SESSIONS[session_id] = {"session_credit": DEFAULT_CREDIT}
    return {"message": "session ID created"}


def get_session_from_request(request):
    """Return saved session data using the session key provided by a request from the frontend."""
    session_id = request.headers.get(SESSION_ID_KEY)
    if session_id is None:
        raise MissingSessionIDException(
            status_code=500,
            detail="Session ID is required. Call /session_id/ endpoint first.",
        )
    session = SESSIONS.get(session_id)
    if session is None:
        raise UnknownSessionIDException(
            status_code=500,
            detail="Unknown session ID.",
        )
    return session
