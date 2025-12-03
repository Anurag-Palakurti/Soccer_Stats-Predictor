import soccerdata as sd
import pandas as pd

def inspect():
    print("📂 Loading cached data...")
    fbref = sd.FBref(leagues="ENG-Premier League", seasons="2425")
    
    # This will be instant because it's already downloaded
    df = fbref.read_player_match_stats(stat_type="summary")
    
    # Reset index to bring "Date" and "Player" out of the index and into columns
    df = df.reset_index()
    
    # Flatten the messy "Multi-Index" columns (e.g. ('Expected', 'xG') -> 'Expected_xG')
    df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns.values]
    
    print("\n✅ DATA LOADED. Here are the available column names:")
    print("="*50)
    
    # Print every column name so we can find the right ones
    for col in df.columns:
        print(f" -> {col}")
        
    print("="*50)
    
    # Try to find the "xG" column automatically
    xg_cols = [c for c in df.columns if "xg" in c.lower()]
    print(f"\n🔍 Columns that look like xG: {xg_cols}")

if __name__ == "__main__":
    inspect()