import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib  # To save the model file

def train_predictor():
    print("🧠 Loading Training Data...")
    df = pd.read_csv("training_data.csv")
    
    # Ensure date is sorted so we don't cheat (train on future data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Player', 'Date'])

    print("⚙️ Feature Engineering (Teaching the AI about 'Form')...")
    
    # 1. Create Lag Features (Moving Averages)
    # We want the model to know: "How did this player do in their LAST 3 games?"
    metrics = ['xG', 'xA', 'Passes', 'Dribbles', 'Minutes']
    
    for metric in metrics:
        # Calculate average of last 3 games
        df[f'Roll_3_{metric}'] = df.groupby('Player')[metric].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean().shift(1)
        )
        # Calculate average of last 10 games (Long term form)
        df[f'Roll_10_{metric}'] = df.groupby('Player')[metric].transform(
            lambda x: x.rolling(window=10, min_periods=1).mean().shift(1)
        )

    # 2. Define the TARGET (What we want to predict)
    # We want to predict the ACTUAL xG of the CURRENT match
    # (The features are from the PREVIOUS matches, so this is valid)
    target_col = 'xG'
    
    # Drop the first few rows for each player (where we don't have enough history yet)
    df = df.dropna()

    print(f"📊 Training on {len(df)} samples...")

    # 3. Split Data
    # Features (X) = The Rolling Averages
    # Target (y) = The Actual xG of that day
    feature_cols = [c for c in df.columns if 'Roll_' in c]
    X = df[feature_cols]
    y = df[target_col]

    # Split: 80% for learning, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    # 4. Train the Model (XGBoost)
    print("🚀 Training XGBoost Model...")
    model = xgb.XGBRegressor(
        n_estimators=500,     # Number of trees
        learning_rate=0.05,   # How fast it learns
        max_depth=5,          # How complex the trees are
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # 5. Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    
    print("\n✅ TRAINING COMPLETE!")
    print(f"   Mean Absolute Error: {mae:.3f}")
    print("   (This means on average, the prediction is off by only this much xG)")

    # 6. Save the Model
    joblib.dump(model, "xg_model.pkl")
    print("💾 Model saved to 'xg_model.pkl'")
    
    # 7. Show a Prediction Example
    print("\n🔮 Sample Prediction vs Reality (Test Set):")
    results = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
    print(results.head(5))

if __name__ == "__main__":
    train_predictor()