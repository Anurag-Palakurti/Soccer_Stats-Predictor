import requests
import json

# Your API Key
API_KEY = "4f96e439cae16aaf73d814db6b93df3c"
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    'x-apisports-key': API_KEY
}

def run_diagnostics():
    print("------- DIAGNOSTICS MODE -------")
    
    # TEST 1: Check Account Status
    print("\n1. Checking Account Status...")
    try:
        status_response = requests.get(f"{BASE_URL}/status", headers=headers)
        status_data = status_response.json()
        
        if 'errors' in status_data and status_data['errors']:
             print(f"❌ API Key Error: {status_data['errors']}")
             return
             
        account = status_data['response']['account']
        requests_info = status_data['response']['requests']
        print(f"✅ Key is Valid! User: {account['firstname']} {account['lastname']}")
        print(f"   Plan: {status_data['response']['subscription']['plan']}")
        print(f"   Requests Today: {requests_info['current']} / {requests_info['limit_day']}")
        
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # TEST 2: Try to get ANY match from the current season (2025)
    # We remove 'last=1' and just ask for the first 5 matches of the season
    print("\n2. Testing Match Data (Season 2025)...")
    params = {
        'league': 39,      # Premier League
        'season': 2025,    # Current Season
        'status': 'FT'     # Finished matches only
    }
    
    # Get just one match, but without the "last" filter which sometimes breaks on older seasons
    r = requests.get(f"{BASE_URL}/fixtures", headers=headers, params=params)
    data = r.json()
    
    if data['response']:
        match = data['response'][0]
        print(f"✅ Success! Found match: {match['teams']['home']['name']} vs {match['teams']['away']['name']}")
        fixture_id = match['fixture']['id']
        
        # TEST 3: Check for xG in this specific match
        print(f"   Checking stats for Fixture ID: {fixture_id}...")
        stats_r = requests.get(f"{BASE_URL}/fixtures/players?fixture={fixture_id}", headers=headers)
        stats_data = stats_r.json()
        
        if stats_data['response']:
            first_player = stats_data['response'][0]['players'][0]['statistics'][0]
            print("\n✅ PLAYER STATS FOUND!")
            # Check for Expected Goals keys
            import json
            print("   Dump of one player's stats keys:")
            print(json.dumps(first_player, indent=2))
        else:
            print("⚠️ Match found, but NO player stats attached (might be a plan limit).")
            
    else:
        print("❌ Still no matches found. The API might be restricting the Premier League for your tier.")
        print("   Full Response:", data)

if __name__ == "__main__":
    run_diagnostics()