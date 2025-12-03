import soccerdata as sd
import pandas as pd
import re

def create_training_set():
    print("⏳ Loading Scraper Data (this will be fast if cached)...")
    
    # 1. Load Data
    fbref = sd.FBref(leagues="ENG-Premier League", seasons="2425")
    df = fbref.read_player_match_stats(stat_type="summary")
    
    # 2. Fix the Columns
    df = df.reset_index()
    # Flatten multi-level columns (e.g., ('Expected', 'xG') -> 'Expected_xG')
    df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns.values]
    
    print("🧹 Cleaning and Renaming Columns...")
    
    # 3. Rename to simple names
    # We map the "Messy Name" -> "Clean Name"
    rename_map = {
        'player_': 'Player',
        'team_': 'Team',
        'game_': 'Match',
        'Performance_Gls': 'Goals',
        'Performance_Ast': 'Assists',
        'Expected_xG': 'xG',
        'Expected_xAG': 'xA',        # This is xA
        'Passes_Cmp': 'Passes',
        'Take-Ons_Succ': 'Dribbles',
        'min_': 'Minutes'
    }
    
    # Select only the columns we need
    # (We use a list comprehension to safe-guard against missing ones)
    cols_to_keep = [c for c in rename_map.keys() if c in df.columns]
    df = df[cols_to_keep].rename(columns=rename_map)
    
    # 4. Extract the Date from the 'Match' column
    # The 'Match' column usually looks like: "2024-08-18 Chelsea 0-2 Manchester City"
    # We grab the first 10 characters (the date part)
    print("📅 Extracting Dates...")
    df['Date'] = df['Match'].astype(str).str[:10]
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # 5. Clean Up
    # Drop rows where Date failed or Minutes is 0 (didn't play)
    df = df.dropna(subset=['Date'])
    df = df[df['Minutes'].astype(float) > 0]
    
    # Sort by Player and Date (CRITICAL for the AI to learn patterns)
    df = df.sort_values(by=['Player', 'Date'])
    
    # 6. Save to CSV
    filename = "training_data.csv"
    df.to_csv(filename, index=False)
    
    print("\n✅ SUCCESS! Master dataset saved as '" + filename + "'")
    print(df[['Date', 'Player', 'xG', 'xA', 'Passes']].head())
    print(f"\nTotal Rows: {len(df)}")

if __name__ == "__main__":
    create_training_set()