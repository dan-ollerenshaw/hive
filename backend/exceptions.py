from fastapi import HTTPException


class MissingSessionIDException(HTTPException):
    pass


class UnknownSessionIDException(HTTPException):
    pass
