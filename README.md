# Coding challenge: Hive Learning

### Backend
- python version: 3.9
- framework: [fastapi](https://fastapi.tiangolo.com/)
- formatting: [black](https://black.readthedocs.io/en/stable/)
- testing: [unittest](https://docs.python.org/3/library/unittest.html)

To launch the API, run this command from the root directory:

`pip install -r requirements.txt` (first time only. ensure a virtual environment is active)

`uvicorn backend.main:app --host 127.0.0.1 --port 8000`

To run the tests, run this command from the root directory:

`pip install -r tests/requirements.txt` (first time only. ensure a virtual environment is active)

`python -m unittest`


### Frontend
- reactJS

To run the frontend, run this command from the frontend directory:

`npm install` (first time only)

`npm start --host localhost --port 3000`


### Assumptions
- default behaviour when app is opened is 10 game credits and 0 credits in the account
- if a user cashes out e.g. 50 session credits, they then have 50 credits in the account and 0 in the session
- if this user then starts a new game, the game is opened with 50 game credits and 0 credits in the account

### Potential improvements
- Remove custom session ID headers. There must be a simpler solution.
- Handle negative credit. At the moment the user will simply go into debt.
- Dockerise the different components.
- Add frontend tests.
