"""
Request and response models for the API.
"""

from pydantic import BaseModel


class RequestModel(BaseModel):
    account_credit: int


class PlayResponseModel(BaseModel):
    session_credit: int
    roll: list


class CashOutResponseModel(BaseModel):
    account_credit: int
