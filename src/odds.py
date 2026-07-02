import httpx
import os
import asyncio
from models import Sport, Region, BettingMarkets
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4"

##the goal is to find the best sportsbook odds per game
async def fetch_odds(sport: Sport, regions: Region = Region.UNITED_STATES, markets: list[BettingMarkets] | None = None):
  async with httpx.AsyncClient() as client:
    try:
      if markets is None:
        markets = [BettingMarkets.MONEYLINE]
      sport = sport.value
      regions = regions.value
      markets = [m.value for m in markets]
      res = await client.get(f"{BASE_URL}/sports/{sport}/odds/", params={"apiKey": API_KEY, "regions": regions, "markets": ','.join(markets)})
      data = res.json()
      if data is None:
        data = {}
      odds_per_game = {}
      for game in data:
        list_of_outcomes = []
        for i in range(len(game['bookmakers'])):
          j = 0
          while j < len(game['bookmakers'][i]['markets']):
            if game['bookmakers'][i]['markets'][j].get('key') in markets:
              list_of_outcomes.append((
                game['bookmakers'][i]['title'],
                game['bookmakers'][i]['markets'][j].get('key'),
                game['bookmakers'][i]['markets'][j].get('outcomes'),
                game['sport_key']
              ))
            j+=1
        odds_per_game[f"{game.get('home_team')}" + ' vs ' + f"{game.get('away_team')}" + ' at ' + f"{game.get('commence_time')}"] = list_of_outcomes
      best_odds_per_game = {}
      for game in odds_per_game.keys():
        best_odds = 0
        best_index = 0
        inner_best_index = 0
        for i in range(len(odds_per_game[game])):
          j = 0
          while j < len(odds_per_game[game][i][2]):
            old_best_odds = best_odds
            best_odds = max(odds_per_game[game][i][2][j].get('price'), old_best_odds)
            if best_odds != old_best_odds:
              best_index = i
              inner_best_index = j
            j+=1
          best_odds_per_game[game] = (odds_per_game[game][best_index][0], odds_per_game[game][best_index][3], odds_per_game[game][best_index][1] ,odds_per_game[game][best_index][2][inner_best_index])
      return best_odds_per_game
    except Exception as e:
      import traceback
      traceback.print_exc()
      print(f"Error: {e}")
