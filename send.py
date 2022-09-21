"""
Test script for the API.

I've modified this to use the custom session ID used by the frontend,
however it's not necessary here. The API will remember the session
over repeated requests, and saved state can easily be accessed
with `requests.session`.
"""


import requests

endpoint = "http://127.0.0.1:8000/"
play = endpoint + "play/"
cash_out = endpoint + "cash_out/"
session_id = endpoint + "session_id/"



if __name__ == "__main__":
    session = requests.Session()
    # get session ID
    res = session.get(session_id)
    session_id = res.headers["x-session-id"]
    # post a few plays
    for _ in range(5):
        res_play = session.post(play, json={"account_credit": 0}, headers={"x-session-id": session_id})
    # cash out
    res_cash = session.get(cash_out, headers={"x-session-id": session_id})
    breakpoint()
