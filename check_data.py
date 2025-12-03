import requests
import json
import pandas as pd

# 1. Setup the connection
api_key = "4f96e439cae16aaf73d814db6b93df3c" # Your key
base_url = "https://v3.football.api-sports.io"

headers = {
    'x-apisports-key': api_key
}

def check_one_match():
    print("SEARCHING for the most recent Premier League match...")
    
    # 2. Get the last played match in the Premier League (League ID 39)
    # We use season 2023 to ensure we get a match with full data
    params = {
        'league': 39, 
        'season': 2023, 
        'last': 1
    }
    
    r = requests.get(f"{base_url}/fixtures", headers=headers, params=params)
    data = r.json()
    
    if not data['response']:
        print("❌ Could not find any matches. Check your plan/quota.")
        return
        
    fixture_id = data['response'][0]['fixture']['id']
    match_date = data['response'][0]['fixture']['date']
    home_team = data['response'][0]['teams']['home']['name']
    away_team = data['response'][0]['teams']['away']['name']
    
    print(f"✅ Found Match: {home_team} vs {away_team} (ID: {fixture_id}) played on {match_date}")
    print("--------------------------------------------------")
    print("📥 Downloading Player Statistics for this match...")
    
    # 3. Get Detailed Player Stats for this fixture
    stats_url = f"{base_url}/fixtures/players"
    stats_params = {'fixture': fixture_id}
    
    r_stats = requests.get(stats_url, headers=headers, params=stats_params)
    stats_data = r_stats.json()
    
    # 4. Parse and Show the Data Structure
    # This will show us EXACTLY what metrics (xG, Dribbles, etc.) we can use.
    if stats_data['response']:
        # Look at the first team, first player
        player_entry = stats_data['response'][0]['players'][0]
        player_name = player_entry['player']['name']
        stats = player_entry['statistics'][0]
        
        print(f"\n🔍 DATA INSPECTION FOR: {player_name}")
        print(f"   (If you see 'None' below, that data point is missing from your plan)")
        print("-" * 40)
        
        # Check for the specific 'Vibe' stats you wanted
        print(f"⚽ Goals:      {stats['goals']['total']}")
        print(f"🎯 Assists:    {stats['goals']['assists']}")
        print(f"👟 Passes:     {stats['passes']['total']} (Accuracy: {stats['passes']['accuracy']}%)")
        print(f"⚡ Dribbles:   {stats['dribbles']['success']} successful (out of {stats['dribbles']['attempts']})")
        print(f"🛑 Tackles:    {stats['tackles']['total']}")
        print(f"🎨 Rating:     {stats['games']['rating']}")
        
        # CRITICAL CHECK FOR xG / xA
        # API-Football often hides xG inside specific 'advanced' endpoints or unexpected keys.
        # Let's check if it exists in the raw dump.
        print("-" * 40)
        print("RAW STATS KEYS (Check here for 'expected_goals'):")
        print(stats.keys())
    else:
        print("❌ No player statistics found for this match.")

if __name__ == "__main__":
    check_one_match()