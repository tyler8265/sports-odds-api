import sqlite3
import json
from datetime import datetime, timezone

def init_db():
  with sqlite3.connect("odds.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          sport TEXT NOT NULL,
          game TEXT NOT NULL,
          data TEXT NOT NULL,
          fetched_at TEXT NOT NULL
        )
    """)

def save_snapshot(game, odds_data):
  curr_time = datetime.now(timezone.utc).isoformat()
  data = json.dumps(odds_data)
  with sqlite3.connect("odds.db") as conn:
    cursor = conn.cursor()
    query = "INSERT INTO snapshots(sport, game, data, fetched_at) VALUES (?, ?, ?, ?);"
    params = (odds_data[1], game, data, curr_time)
    cursor.execute(query, params)

def get_snapshots(game=None):
  snapshots = []
  with sqlite3.connect("odds.db") as conn:
    cursor = conn.cursor()
    if(game):
      cursor.execute("SELECT * FROM snapshots WHERE game LIKE ?", (f"%{game}%",))
    else:
      cursor.execute("SELECT * FROM snapshots")
    rows = cursor.fetchall()
    for row in rows:
      row = list(row)
      row[3] = json.loads(row[3])
      snapshots.append(row)
  return snapshots

if __name__ == "__main__":
  init_db()
