import soccerdata as sd
import pandas as pd

def fetch_current_stats():
    print("⏳ Starting Scraper... (This takes 10-20 seconds unlike an API)")
    
    # 1. Initialize the FBref Scraper for the Premier League (24/25)
    # FBref uses the code 'ENG-Premier League'
    fbref = sd.FBref(leagues="ENG-Premier League", seasons="2425")
    
    print("📥 Downloading Player Match Logs (The Holy Grail of Data)...")
    
    # 2. distinct from 'season_stats', 'read_player_match_stats' gets EVERY game
    # stat_type="summary" gives us Goals, Assists, xG, xA, Shots, Passes
    try:
        df = fbref.read_player_match_stats(stat_type="summary")
    except Exception as e:
        print(f"❌ Scraping Error: {e}")
        print("Tip: FBref sometimes blocks if you run this too fast. Wait 1 min and try again.")
        return None

    # 3. Clean and Show the Data
    # The scraper returns a complex "MultiIndex", let's flatten it for simplicity
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    df = df.reset_index()

    # Filter for a specific star to verify it worked (e.g., Haaland or Salah)
    # We look for columns like 'Performance_Gls' (Goals) and 'Expected_xG'
    print("\n✅ DATA SUCCESS! Here is a sample (Haaland's last 3 games):")
    
    target_player = df[df['player'].str.contains("Haaland", na=False)]
    
    if not target_player.empty:
        # Show specific "Vibe" columns
        cols_to_show = ['date', 'round', 'player', 'Performance_Gls', 'Expected_xG', 'Expected_xA']
        print(target_player[cols_to_show].tail(3))
    else:
        print("Could not find Haaland, but here is the first row:")
        print(df.head(1))
        
    return df

if __name__ == "__main__":
    data = fetch_current_stats()