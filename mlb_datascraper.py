from datetime import datetime
import requests


def get_daily_mlb_matchups():
    # 1. Dynamically get today's date in YYYY-MM-DD format
    today = datetime.today().strftime("%Y-%m-%d")
    print(f"=== Fetching MLB Matchups for Today: {today} ===\n")

    # 2. Query the MLB Schedule API for today's games
    schedule_url = f"https://mlb.com{today}&hydrate=probablePitcher,lineups"
    response = requests.get(schedule_url)

    if response.status_code != 200:
        print("Error: Could not fetch data from MLB API.")
        return

    data = response.json()
    dates = data.get("dates", [])

    if not dates:
        print("No games scheduled for today.")
        return

    games = dates[0].get("games", [])
    print(f"Found {len(games)} scheduled games.\n")

    # 3. Loop through each game to extract matchup details
    for game in games:
        game_id = game.get("gamePk")
        venue = game.get("venue", {}).get("name", "Unknown Stadium")

        # Team names
        away_team = game["teams"]["away"]["team"]["name"]
        home_team = game["teams"]["home"]["team"]["name"]

        # Extract probable pitchers safely
        away_pitcher_data = game["teams"]["away"].get("probablePitcher", {})
        home_pitcher_data = game["teams"]["home"].get("probablePitcher", {})

        away_pitcher = away_pitcher_data.get("fullName", "TBD")
        home_pitcher = home_pitcher_data.get("fullName", "TBD")

        # Fetch Pitcher Details (Throws Right or Left)
        away_pitcher_hand = get_pitcher_hand(away_pitcher_data.get("id"))
        home_pitcher_hand = get_pitcher_hand(home_pitcher_data.get("id"))

        # Print clean, scannable overview
        print(f"🏟️  Matchup: {away_team} @ {home_team}")
        print(f"📍 Location: {venue}")
        print(
            f"🪓 Away Pitcher: {away_pitcher} ({away_pitcher_hand}-Handed)"
        )
        print(
            f"🏠 Home Pitcher: {home_pitcher} ({home_pitcher_hand}-Handed)"
        )
        print(
            f"🔗 Live Data Link: https://mlb.com{game_id}"
        )
        print("-" * 50)


def get_pitcher_hand(player_id):
    """Helper function to fetch if a pitcher throws Left or Right."""
    if not player_id:
        return "Unknown"

    player_url = f"https://mlb.com{player_id}"
    try:
        res = requests.get(player_url).json()
        hand = res["people"][0].get("pitchHand", {}).get("code", "U")
        return "Left" if hand == "L" else "Right"
    except Exception:
        return "Unknown"


if __name__ == "__main__":
    get_daily_mlb_matchups()
