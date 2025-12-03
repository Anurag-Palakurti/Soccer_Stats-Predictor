import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

def train_all_metrics():
    print("🧠 Loading Data for Multi-Target Training...")
    df = pd.read_csv("training_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Player', 'Date'])
    
    # 1. Setup the Features (The Inputs)
    # We use the same rolling averages as before
    feature_metrics = ['xG', 'xA', 'Passes', 'Dribbles', 'Minutes']
    
    print("⚙️ Engineering Features...")
    for m in feature_metrics:
        df[f'Roll_3_{m}'] = df.groupby('Player')[m].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean().shift(1)
        )
    
    df = df.dropna()
    
    # The list of things we want to predict
    targets = ['xG', 'xA', 'Passes', 'Dribbles']
    
    print(f"📊 Training {len(targets)} separate models on {len(df)} rows...")
    
    for target in targets:
        print(f"\n🚀 Training Model for: {target.upper()}...")
        
        # Prepare inputs (X) and target (y)
        feature_cols = [c for c in df.columns if 'Roll_' in c]
        X = df[feature_cols]
        y = df[target]
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        # Train
        model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.05, n_jobs=-1)
        model.fit(X_train, y_train)
        
        # Evaluate
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        print(f"   ✅ {target} MAE: {mae:.3f}")
        
        # Save
        filename = f"model_{target}.pkl"
        joblib.dump(model, filename)
        print(f"   💾 Saved to {filename}")

if __name__ == "__main__":
    train_all_metrics()