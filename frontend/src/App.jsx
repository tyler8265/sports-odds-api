import { useState, useEffect } from "react";

const API_BASE = "/api";

const SPORTS = [
  { label: "NFL", value: "americanfootball_nfl" },
  { label: "NFL Preseason", value: "americanfootball_nfl_preseason" },
  { label: "NCAAF", value: "americanfootball_ncaaf" },
  { label: "CFL", value: "americanfootball_cfl" },
  { label: "UFL", value: "americanfootball_ufl" },
  { label: "NBA", value: "basketball_nba" },
  { label: "NBA Preseason", value: "basketball_nba_preseason" },
  { label: "NBA Summer League", value: "basketball_nba_summer_league" },
  { label: "NCAAB", value: "basketball_ncaab" },
  { label: "WNBA", value: "basketball_wnba" },
  { label: "Euroleague", value: "basketball_euroleague" },
  { label: "NBL", value: "basketball_nbl" },
  { label: "MLB", value: "baseball_mlb" },
  { label: "MLB Preseason", value: "baseball_mlb_preseason" },
  { label: "NHL", value: "icehockey_nhl" },
  { label: "NHL Preseason", value: "icehockey_nhl_preseason" },
  { label: "UFC/MMA", value: "mma_mixed_martial_arts" },
  { label: "AFL", value: "aussierules_afl" },
  { label: "NRL", value: "rugbyleague_nrl" },
  { label: "MLS", value: "soccer_usa_mls" },
  { label: "EPL", value: "soccer_epl" },
  { label: "La Liga", value: "soccer_spain_la_liga" },
  { label: "Bundesliga", value: "soccer_germany_bundesliga" },
  { label: "Serie A", value: "soccer_italy_serie_a" },
  { label: "Ligue 1", value: "soccer_france_ligue_one" },
  { label: "Champions League", value: "soccer_uefa_champs_league" },
  { label: "Europa League", value: "soccer_uefa_europa_league" },
  { label: "Liga MX", value: "soccer_mexico_ligamx" },
  { label: "Eredivisie", value: "soccer_netherlands_eredivisie" },
  { label: "Primeira Liga", value: "soccer_portugal_primeira_liga" },
  { label: "Saudi Pro League", value: "soccer_saudi_arabia_pro_league" },
  { label: "Copa Libertadores", value: "soccer_conmebol_copa_libertadores" },
  { label: "World Cup", value: "soccer_fifa_world_cup" },
];

const MARKETS = [
  { label: "Moneyline", value: "h2h" },
  { label: "Spread", value: "spreads" },
  { label: "Over/Under", value: "totals" },
  { label: "Futures", value: "outrights" },
  { label: "Moneyline Lay", value: "h2h_lay" },
  { label: "Futures Lay", value: "outrights_lay" },
  { label: "Alt Spreads", value: "alternate_spreads" },
  { label: "Alt Totals", value: "alternate_totals" },
  { label: "Both Teams Score", value: "btts" },
  { label: "Draw No Bet", value: "draw_no_bet" },
  { label: "3-Way", value: "h2h_3_way" },
  { label: "Team Totals", value: "team_totals" },
  { label: "Alt Team Totals", value: "alternate_team_totals" },
];

const MARKET_LABELS = {
  h2h: "ML", spreads: "SPR", totals: "O/U", outrights: "FUT",
  h2h_lay: "ML-L", outrights_lay: "FUT-L", alternate_spreads: "A-SPR",
  alternate_totals: "A-O/U", btts: "BTS", draw_no_bet: "DNB",
  h2h_3_way: "3W", team_totals: "TT", alternate_team_totals: "A-TT",
};

const REGIONS = [
  { label: "United States", value: "us" },
  { label: "United States (Exchange)", value: "us_ex" },
  { label: "United States (DFS)", value: "us_dfs" },
  { label: "United States 2", value: "us_2" },
  { label: "United Kingdom", value: "uk" },
  { label: "Europe", value: "eu" },
  { label: "France", value: "fr" },
  { label: "Sweden", value: "se" },
  { label: "Australia", value: "au" },
];

function Badge({ text }) {
  const colors = {
    h2h: "bg-emerald-900 text-emerald-300 border border-emerald-700",
    spreads: "bg-blue-900 text-blue-300 border border-blue-700",
    totals: "bg-purple-900 text-purple-300 border border-purple-700",
    outrights: "bg-yellow-900 text-yellow-300 border border-yellow-700",
    h2h_3_way: "bg-orange-900 text-orange-300 border border-orange-700",
    btts: "bg-pink-900 text-pink-300 border border-pink-700",
  };
  return (
    <span className={`text-xs font-mono px-2 py-0.5 rounded ${colors[text] || "bg-zinc-800 text-zinc-400"}`}>
      {MARKET_LABELS[text] || text}
    </span>
  );
}

function OddsCard({ game, data }) {
  const [bookmaker, sport, market, outcome] = data;
  const [stake, setStake] = useState("");
  const teams = game.split(" at ")[0];
  const time = game.split(" at ")[1];
  const date = time ? new Date(time).toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }) : "";

  const price = outcome?.price;
  const stakeNum = parseFloat(stake);
  const hasStake = stake && !isNaN(stakeNum) && stakeNum > 0 && price;
  const payout = hasStake ? (stakeNum * price).toFixed(2) : null;
  const profit = hasStake ? (stakeNum * price - stakeNum).toFixed(2) : null;

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4 hover:border-zinc-600 transition-colors">
      <div className="flex items-start justify-between gap-2 mb-3">
        <p className="text-sm font-semibold text-white leading-tight">{teams}</p>
        <Badge text={market} />
      </div>
      <div className="flex items-end justify-between mb-3">
        <div>
          <p className="text-xs text-zinc-500 mb-1">{bookmaker}</p>
          <p className="text-zinc-300 text-sm">{outcome?.name}</p>
          {outcome?.point !== undefined && (
            <p className="text-xs text-zinc-500">{outcome.point > 0 ? `+${outcome.point}` : outcome.point}</p>
          )}
        </div>
        <div className="text-right">
          {payout ? (
            <>
              <p className="text-xs text-zinc-500 mb-0.5">payout</p>
              <p className="text-2xl font-mono font-bold text-emerald-400">${payout}</p>
            </>
          ) : (
            <>
              <p className="text-xs text-zinc-500 mb-0.5">odds</p>
              <p className="text-2xl font-mono font-bold text-emerald-400">{price?.toFixed(2)}</p>
            </>
          )}
          <p className="text-xs text-zinc-600">{date}</p>
        </div>
      </div>

      <div className="border-t border-zinc-800 pt-3">
        <div className="flex items-center gap-3">
          <div className="relative flex-1">
            <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500 text-sm">$</span>
            <input
              type="number"
              min="0"
              placeholder="Stake"
              value={stake}
              onChange={(e) => setStake(e.target.value)}
              className="w-full bg-zinc-800 border border-zinc-700 text-white text-sm rounded-lg pl-6 pr-3 py-1.5 focus:outline-none focus:border-zinc-500 placeholder-zinc-600"
            />
          </div>
          {profit && (
            <div className="text-right shrink-0">
              <p className="text-xs text-zinc-500">profit</p>
              <p className="text-xl font-mono font-bold text-blue-400">+${profit}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function HistoryCard({ row }) {
  const [id, sport, game, dataRaw, fetchedAt] = row;
  const data = typeof dataRaw === "string" ? JSON.parse(dataRaw) : dataRaw;
  const [bookmaker, sportKey, market, outcome] = data;
  const date = new Date(fetchedAt).toLocaleString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
      <div className="flex items-start justify-between gap-2 mb-2">
        <p className="text-sm font-semibold text-white leading-tight">{game.split(" at ")[0]}</p>
        <Badge text={market} />
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className="text-xs text-zinc-500">{bookmaker}</p>
          <p className="text-zinc-300 text-sm">{outcome?.name}</p>
        </div>
        <div className="text-right">
          <p className="text-xl font-mono font-bold text-blue-400">{outcome?.price?.toFixed(2)}</p>
          <p className="text-xs text-zinc-600">Fetched {date}</p>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [tab, setTab] = useState("odds");
  const [sport, setSport] = useState("americanfootball_nfl");
  const [region, setRegion] = useState("us");
  const [markets, setMarkets] = useState(["h2h"]);
  const [odds, setOdds] = useState(null);
  const [history, setHistory] = useState(null);
  const [historyGames, setHistoryGames] = useState([]);
  const [historyQuery, setHistoryQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (tab === "history" && historyGames.length === 0) {
      fetch(`${API_BASE}/odds/history/games`)
        .then((r) => r.json())
        .then((json) => setHistoryGames(json.games || []));
    }
  }, [tab]);

  function toggleMarket(val) {
    setMarkets((prev) =>
      prev.includes(val) ? prev.filter((m) => m !== val) : [...prev, val]
    );
  }

  async function fetchOdds() {
    if (!markets.length) return;
    setLoading(true);
    setError(null);
    setOdds(null);
    try {
      const params = new URLSearchParams();
      markets.forEach((m) => params.append("markets", m));
      params.append("region", region);
      const res = await fetch(`${API_BASE}/odds/${sport}?${params}`);
      const json = await res.json();
      setOdds(json.odds || {});
    } catch (e) {
      setError("Failed to reach the API.");
    } finally {
      setLoading(false);
    }
  }

  async function fetchHistory() {
    if (!historyQuery) return;
    setLoading(true);
    setError(null);
    setHistory(null);
    try {
      const res = await fetch(`${API_BASE}/odds/history?game=${encodeURIComponent(historyQuery)}`);
      const json = await res.json();
      setHistory(json["historical snapshots"] || []);
    } catch (e) {
      setError("Failed to reach the API.");
    } finally {
      setLoading(false);
    }
  }

  const oddsEntries = odds ? Object.entries(odds) : [];

  return (
    <div className="min-h-screen bg-black text-white">
      <header className="border-b border-zinc-800 px-6 py-4 flex flex-wrap items-center justify-between gap-3">
        <div className="shrink-0">
          <h1 className="text-lg font-bold tracking-tight text-white font-mono">ODDS//API</h1>
          <p className="text-xs text-zinc-500">Best lines across bookmakers, live</p>
        </div>
        <div className="flex gap-1 bg-zinc-900 border border-zinc-800 rounded-lg p-1">
          {["odds", "history"].map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-1.5 rounded text-sm font-medium transition-colors ${
                tab === t ? "bg-zinc-700 text-white" : "text-zinc-400 hover:text-white"
              }`}
            >
              {t === "odds" ? "Live Odds" : "History"}
            </button>
          ))}
        </div>
      </header>

      <main className="px-6 py-8">
        {tab === "odds" && (
          <>
            <div className="flex flex-wrap gap-4 mb-6">
              <div>
                <label className="text-xs text-zinc-500 block mb-1.5 uppercase tracking-widest">Sport</label>
                <select
                  value={sport}
                  onChange={(e) => setSport(e.target.value)}
                  className="bg-zinc-900 border border-zinc-700 text-white text-sm rounded-lg px-3 py-2 focus:outline-none focus:border-zinc-500"
                >
                  {SPORTS.map((s) => (
                    <option key={s.value} value={s.value}>{s.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-zinc-500 block mb-1.5 uppercase tracking-widest">Region</label>
                <select
                  value={region}
                  onChange={(e) => setRegion(e.target.value)}
                  className="bg-zinc-900 border border-zinc-700 text-white text-sm rounded-lg px-3 py-2 focus:outline-none focus:border-zinc-500"
                >
                  {REGIONS.map((r) => (
                    <option key={r.value} value={r.value}>{r.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-zinc-500 block mb-1.5 uppercase tracking-widest">Markets</label>
                <div className="flex flex-wrap gap-2">
                  {MARKETS.map((m) => (
                    <button
                      key={m.value}
                      onClick={() => toggleMarket(m.value)}
                      className={`px-3 py-2 text-sm rounded-lg border transition-colors ${
                        markets.includes(m.value)
                          ? "bg-zinc-700 border-zinc-500 text-white"
                          : "bg-zinc-900 border-zinc-700 text-zinc-400 hover:text-white"
                      }`}
                    >
                      {m.label}
                    </button>
                  ))}
                </div>
              </div>
              <div className="flex items-end">
                <button
                  onClick={fetchOdds}
                  disabled={loading || !markets.length}
                  className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-semibold px-5 py-2 rounded-lg transition-colors"
                >
                  {loading ? "Fetching..." : "Get Odds"}
                </button>
              </div>
            </div>

            {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

            {odds && (
              <div className="mb-2">
                <p className="text-xs text-zinc-500">{oddsEntries.length} games</p>
              </div>
            )}

            {oddsEntries.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {oddsEntries.map(([game, data]) => (
                  <OddsCard key={game} game={game} data={data} />
                ))}
              </div>
            )}

            {odds && oddsEntries.length === 0 && (
              <p className="text-zinc-500 text-sm">No games found for this sport and market combination.</p>
            )}
          </>
        )}

        {tab === "history" && (
          <>
            <div className="flex gap-3 mb-6">
              <div className="flex-1">
                <label className="text-xs text-zinc-500 block mb-1.5 uppercase tracking-widest">Select Game</label>
                <select
                  value={historyQuery}
                  onChange={(e) => setHistoryQuery(e.target.value)}
                  className="w-full bg-zinc-900 border border-zinc-700 text-white text-sm rounded-lg px-3 py-2 focus:outline-none focus:border-zinc-500"
                >
                  <option value="">-- Select a game --</option>
                  {historyGames.map((g) => (
                    <option key={g} value={g}>{g.split(" at ")[0]}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={fetchHistory}
                  disabled={loading || !historyQuery}
                  className="bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white text-sm font-semibold px-5 py-2 rounded-lg transition-colors"
                >
                  {loading ? "Loading..." : "Load Snapshots"}
                </button>
              </div>
            </div>

            {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

            {history && history.length === 0 && (
              <p className="text-zinc-500 text-sm">No snapshots found for this game.</p>
            )}

            {history && history.length > 0 && (
              <>
                <p className="text-xs text-zinc-500 mb-3">{history.length} snapshots</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {history.map((row) => (
                    <HistoryCard key={row[0]} row={row} />
                  ))}
                </div>
              </>
            )}
          </>
        )}
      </main>
    </div>
  );
}
