"""
Tests for the backend API.

Note: for these tests I launch the API as a background process.
It would be more common to test against an existing, deployed version of the API.
"""

import ast
import subprocess
import unittest

import requests


API_HOST = "127.0.0.1"
API_PORT = "8000"
BASE_URL = f"http://{API_HOST}:{API_PORT}/"
PLAY_ENDPOINT = BASE_URL + "play/"
CASH_OUT_ENDPOINT = BASE_URL + "cash_out/"
SESSION_ENDPOINT = BASE_URL + "session_id/"


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_process = subprocess.Popen(
            ["uvicorn", "backend.main:app", "--host", API_HOST, "--port", API_PORT]
        )

    def setUp(self):
        self.session = requests.Session()

    def test_all_endpoints(self):
        """Test reaching all 3 endpoints in the expected order."""
        resp_session = self.session.get(SESSION_ENDPOINT)
        session_id = resp_session.headers["x-session-id"]
        resp_play = self.session.post(
            PLAY_ENDPOINT,
            json={"account_credit": 0},
            headers={"x-session-id": session_id},
        )
        resp_cash = self.session.get(
            CASH_OUT_ENDPOINT, headers={"x-session-id": session_id}
        )
        for response in [resp_session, resp_play, resp_cash]:
            self.assertEqual(response.status_code, 200)

    def test_play(self):
        """Test that the play endpoint returns valid credit and roll values."""
        resp_session = self.session.get(SESSION_ENDPOINT)
        session_id = resp_session.headers["x-session-id"]
        resp_play = self.session.post(
            PLAY_ENDPOINT,
            json={"account_credit": 0},
            headers={"x-session-id": session_id},
        )
        data = resp_play.json()
        self.assertIsInstance(data.get("session_credit"), int)
        self.assertIsInstance(data.get("roll"), list)

    def test_play_missing_data(self):
        """Test that the play endpoint returns a 422 from a request with missing data."""
        resp_session = self.session.get(SESSION_ENDPOINT)
        session_id = resp_session.headers["x-session-id"]
        resp_play = self.session.post(
            PLAY_ENDPOINT,
            json={},
            headers={"x-session-id": session_id},
        )
        self.assertEqual(resp_play.status_code, 422)
        message = ast.literal_eval(resp_play.text)
        self.assertEqual(
            message,
            {
                "detail": [
                    {
                        "loc": ["body", "account_credit"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        )

    def test_cash_out(self):
        """Test that the cash out endpoint returns a valid account credit value."""
        resp_session = self.session.get(SESSION_ENDPOINT)
        session_id = resp_session.headers["x-session-id"]
        resp_cash = self.session.get(
            CASH_OUT_ENDPOINT, headers={"x-session-id": session_id}
        )
        data = resp_cash.json()
        self.assertIsInstance(data.get("account_credit"), int)

    def test_missing_session_id(self):
        response = self.session.post(
            PLAY_ENDPOINT, json={"account_credit": 0}, headers={}
        )
        self.assertEqual(response.status_code, 500)
        message = ast.literal_eval(response.text)
        self.assertEqual(
            message,
            {"detail": "Session ID is required. Call /session_id/ endpoint first."},
        )

    def test_unknown_session_id(self):
        response = self.session.post(
            PLAY_ENDPOINT,
            json={"account_credit": 0},
            headers={"x-session-id": "unknownid123"},
        )
        self.assertEqual(response.status_code, 500)
        message = ast.literal_eval(response.text)
        self.assertEqual(message, {"detail": "Unknown session ID."})

    @classmethod
    def tearDownClass(cls):
        cls.api_process.kill()
