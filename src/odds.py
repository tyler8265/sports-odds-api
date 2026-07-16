import httpx
import os
import asyncio
from pydantic import BaseModel
from models import Sport, Region, BettingMarkets
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4"

##named result shape (instead of a positional tuple) so API consumers, e.g. Go structs, can bind by field name
class BestOdds(BaseModel):
  bookmaker: str
  sport: str
  market: str
  outcome: dict

###all winnings are based off of a 1.00 bet, so the winnings shown can just be used as a multiplier
def calculate_winnings(bet: float, multiplier: float):
  if bet > 0.0:
    return bet * multiplier
  else:
    print("Not an acceptable bet. Please place a bet above 0.")
    return 0.0

##the goal is to find the best sportsbook odds per game
async def fetch_odds(sport: Sport, regions: Region = Region.UNITED_STATES, markets: list[BettingMarkets] | None = None):
  async with httpx.AsyncClient() as client:
    try:
      if markets is None:
        markets = [BettingMarkets.MONEYLINE]
      sports_str: str = sport.value
      regions_str: str = regions.value
      markets_str: str = [m.value for m in markets]

      all_data = {}
      for market in markets:
        res = await client.get(f"{BASE_URL}/sports/{sport.value}/odds/", params={"apiKey": API_KEY, "regions": regions.value, "markets": market.value, "oddsFormat": "decimal"})
        data = res.json()
        if not isinstance(data, list):
          continue
        for game in data:
          game_key = f"{game.get('home_team')} vs {game.get('away_team')} at {game.get('commence_time')}"
          if game_key not in all_data:
            all_data[game_key] = game
          else:
            all_data[game_key]['bookmakers'].extend(game['bookmakers'])

      odds_per_game = {}
      for game_key, game in all_data.items():
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
        if not list_of_outcomes:
          continue
        odds_per_game[game_key] = list_of_outcomes

      best_odds_per_game = {}
      for game in odds_per_game.keys():
        best_bets = {}
        for i in range(len(odds_per_game[game])):
          bookmaker = odds_per_game[game][i][0]
          market = odds_per_game[game][i][1]
          outcomes = odds_per_game[game][i][2]
          sport_key = odds_per_game[game][i][3]
          j = 0
          while j < len(outcomes):
            bet_key = (market, outcomes[j].get('name'))
            if bet_key not in best_bets or outcomes[j].get('price') > best_bets[bet_key].outcome.get('price'):
              best_bets[bet_key] = BestOdds(
                bookmaker=bookmaker,
                sport=sport_key,
                market=market,
                outcome=outcomes[j]
              )
            j+=1
        best_odds_per_game[game] = list(best_bets.values())
      return best_odds_per_game
    except Exception as e:
      import traceback
      traceback.print_exc()
      print(f"Error: {e}")
