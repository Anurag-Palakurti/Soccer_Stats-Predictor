import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration
st.set_page_config(page_title="Pro Player Predictor", layout="wide")

# 2. Load Data & Models
@st.cache_data
def load_data():
    df = pd.read_csv("training_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@st.cache_resource
def load_models():
    models = {
        'xG': joblib.load("model_xG.pkl"),
        'xA': joblib.load("model_xA.pkl"),
        'Passes': joblib.load("model_Passes.pkl"),
        'Dribbles': joblib.load("model_Dribbles.pkl")
    }
    return models

df = load_data()
models = load_models()

# --- SIDEBAR ---
st.sidebar.title("⚽ Player Scout")
st.sidebar.markdown("### 1. Primary Player")
team_list = sorted(df['Team'].unique())
team1 = st.sidebar.selectbox("Select Team", team_list, key="team1")
player_list1 = sorted(df[df['Team'] == team1]['Player'].unique())
player1 = st.sidebar.selectbox("Select Player", player_list1, key="p1")

# Comparison Toggle
st.sidebar.markdown("---")
compare_mode = st.sidebar.checkbox("🔓 Unlock Comparison Mode")

player2 = None
if compare_mode:
    st.sidebar.markdown("### 2. Comparison Player")
    team2 = st.sidebar.selectbox("Select Opponent Team", team_list, key="team2", index=1)
    player_list2 = sorted(df[df['Team'] == team2]['Player'].unique())
    player2 = st.sidebar.selectbox("Select Opponent", player_list2, key="p2")

# --- HELPER FUNCTION ---
def get_prediction(player_name, models, df):
    stats = df[df['Player'] == player_name].sort_values(by='Date')
    if len(stats) < 3:
        return None, stats
    
    last_3 = stats.tail(3)
    features = pd.DataFrame({
        'Roll_3_xG': [last_3['xG'].mean()],
        'Roll_3_xA': [last_3['xA'].mean()],
        'Roll_3_Passes': [last_3['Passes'].mean()],
        'Roll_3_Dribbles': [last_3['Dribbles'].mean()],
        'Roll_3_Minutes': [last_3['Minutes'].mean()]
    })
    
    preds = {
        'xG': models['xG'].predict(features)[0],
        'xA': models['xA'].predict(features)[0],
        'Passes': models['Passes'].predict(features)[0],
        'Dribbles': models['Dribbles'].predict(features)[0]
    }
    return preds, stats

# --- MAIN UI ---
st.title("⚽ AI Match Predictor")

# Get Data for Player 1
p1_preds, p1_stats = get_prediction(player1, models, df)

if not compare_mode:
    # --- SINGLE PLAYER VIEW (ORIGINAL) ---
    st.subheader(f"🚀 {player1} Analysis")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Predicted xG", f"{p1_preds['xG']:.2f}")
    col2.metric("Predicted xA", f"{p1_preds['xA']:.2f}")
    col3.metric("Passes", f"{int(p1_preds['Passes'])}")
    col4.metric("Dribbles", f"{p1_preds['Dribbles']:.1f}")

    st.subheader("📈 Season Trend")
    fig, ax = plt.subplots(figsize=(10, 3))
    sns.lineplot(data=p1_stats, x='Date', y='xG', marker='o', label='Actual xG', ax=ax)
    ax.axhline(p1_preds['xG'], color='red', linestyle='--', label='Next Match Prediction')
    st.pyplot(fig)

else:
    # --- COMPARISON VIEW (NEW) ---
    p2_preds, p2_stats = get_prediction(player2, models, df)
    
    st.subheader(f"⚔️ Head-to-Head: {player1} vs {player2}")
    
    # Create 3 columns: Player 1 | Metric Name | Player 2
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"<h3 style='text-align: center;'>{player1}</h3>", unsafe_allow_html=True)
        st.metric("xG", f"{p1_preds['xG']:.2f}")
        st.metric("Assists (xA)", f"{p1_preds['xA']:.2f}")
        st.metric("Passes", f"{int(p1_preds['Passes'])}")
        
    with col3:
        st.markdown(f"<h3 style='text-align: center;'>{player2}</h3>", unsafe_allow_html=True)
        # Green delta if Player 2 is better, Red if worse
        st.metric("xG", f"{p2_preds['xG']:.2f}", delta=f"{p2_preds['xG'] - p1_preds['xG']:.2f}")
        st.metric("Assists (xA)", f"{p2_preds['xA']:.2f}", delta=f"{p2_preds['xA'] - p1_preds['xA']:.2f}")
        st.metric("Passes", f"{int(p2_preds['Passes'])}", delta=f"{int(p2_preds['Passes'] - p1_preds['Passes'])}")

    # Comparison Chart
    st.subheader("📊 Form Comparison (Last 5 Games xG)")
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Plot both lines
    sns.lineplot(data=p1_stats.tail(10), x='Date', y='xG', marker='o', label=player1, ax=ax)
    sns.lineplot(data=p2_stats.tail(10), x='Date', y='xG', marker='o', label=player2, ax=ax)
    
    ax.set_ylabel("Expected Goals (xG)")
    st.pyplot(fig)