import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4"

##the goal is to find the best sportsbook odds per game
async def fetch_odds(sport: str, regions: str = "us", markets: list = ["h2h"]):
  async with httpx.AsyncClient() as client:
    try:
      res = await client.get(f"{BASE_URL}/sports/{sport}/odds/", params={"apiKey": API_KEY, "regions": regions, "markets": ','.join(markets)})
      data = res.json()
      odds_per_game = {}
      for game in data:
        list_of_outcomes = []
        for i in range(len(game['bookmakers'])):
          j = 0
          while j < len(game['bookmakers'][i]['markets']):
            if game['bookmakers'][i]['markets'][j].get('key') in markets:
              list_of_outcomes.append((game['bookmakers'][i]['title'] , game['bookmakers'][i]['markets'][j].get('outcomes')))
            j+=1
        odds_per_game[f"{game.get('id')}" + '___' + f"{game.get('commence_time')}"] = list_of_outcomes
      best_odds_per_game = {}
      for game in odds_per_game.keys():
        best_odds = 0
        best_index = 0
        inner_best_index = 0
        for i in range(len(odds_per_game.get(game))):
          j = 0
          while j < len(odds_per_game.get(game)[i][1]):
            old_best_odds = best_odds
            best_odds = max(odds_per_game.get(game)[i][1][j].get('price'), old_best_odds)
            if best_odds != old_best_odds:
              best_index = i
              inner_best_index = j
            j+=1
          best_odds_per_game[game] = (odds_per_game.get(game)[best_index][0] ,odds_per_game.get(game)[best_index][1][inner_best_index])
      return best_odds_per_game
    except httpx.RequestError as e:
      print(f"Request failed: {e}")
