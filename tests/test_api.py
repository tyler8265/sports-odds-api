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
    assert isinstance(first_game[0], str)  # bookmaker name
    assert isinstance(first_game[1], str)  # sport key
    assert isinstance(first_game[2], str)  # market key
    assert isinstance(first_game[3], dict)  # outcome

def test_invalid_sport():
    res = client.get("/odds/fake_sport")
    assert res.status_code == 422
