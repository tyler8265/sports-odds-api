from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock, patch

with patch("db.init_db"), patch("db.get_conn"):
  from fastapi.testclient import TestClient
  from main import app

client = TestClient(app)

@patch("db.save_snapshot")
def test_get_odds(mock_save):
    mock_save.return_value = None
    res = client.get("/odds/americanfootball_nfl")
    assert res.status_code == 200
    assert "odds" in res.json()

@patch("db.save_snapshot")
def test_odds_response_shape(mock_save):
    mock_save.return_value = None
    res = client.get("/odds/americanfootball_nfl")
    odds = res.json()["odds"]
    first_game = list(odds.values())[0]
    assert isinstance(first_game[0], str)  # bookmaker name
    assert isinstance(first_game[1], str)  # sport key
    assert isinstance(first_game[2], str)  # market key
    assert isinstance(first_game[3], dict)  # outcome

def test_invalid_sport():
    res = client.get("/odds/fake_sport")
    assert res.status_code == 422
