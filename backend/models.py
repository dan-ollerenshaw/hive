"""
Request and response models for the API.
"""

from pydantic import BaseModel

from backend.slot_machine import DEFAULT_CREDIT


class GameModel(BaseModel):
    credit: int = DEFAULT_CREDIT
