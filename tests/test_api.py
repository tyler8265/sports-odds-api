import sys
from unittest.mock import MagicMock, patch

# Patch before any imports that trigger db connection
sys.modules['db'] = MagicMock()

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_odds():
    res = client.get("/odds/americanfootball_nfl")
    assert res.status_code == 200
    assert "odds" in res.json()

def test_odds_response_shape():
    res = client.get("/odds/americanfootball_nfl")
    odds = res.json()["odds"]
    first_game = list(odds.values())[0]
    assert isinstance(first_game[0], str)
    assert isinstance(first_game[1], str)
    assert isinstance(first_game[2], str)
    assert isinstance(first_game[3], dict)

def test_invalid_sport():
    res = client.get("/odds/fake_sport")
    assert res.status_code == 422
