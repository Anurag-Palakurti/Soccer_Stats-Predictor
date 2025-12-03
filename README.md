# Soccer_Stats-Predictor
Predicts Premier League player performance using XGBoost to forecast goals, assists, passes, and dribbles. Includes advanced feature engineering on 11k+ match records and an interactive Streamlit dashboard for real-time predictions and player comparisons.
# Player Performance Predictor

The Premier League Player Performance Predictor is a machine learning project designed to forecast key player statistics, including goals, assists, passes, and dribbles. Built using an XGBoost-based multi-target regression model, the system leverages advanced temporal feature engineering and over 11,000 match records collected from FBref. An interactive Streamlit dashboard is included to provide real-time prediction capabilities, player filtering, and head-to-head comparison tools for performance analysis.

This project demonstrates applied machine learning, data engineering, and full-stack deployment within a sports analytics context. It is intended for researchers, data scientists, football analysts, and anyone interested in predictive modeling for player performance.

---

## Features

- Multi-target prediction for goals, assists, passes, and dribbles using gradient-boosted regression.
- Achieves a Mean Absolute Error (MAE) of 0.095 on Expected Goals (xG) forecasting.
- Temporal feature engineering incorporating rolling averages, lag features, and form-based metrics.
- Automated ETL pipeline for scraping, cleaning, and normalizing Premier League match data using soccerdata and Pandas.
- Interactive Streamlit dashboard for real-time inference, dynamic player filtering, and side-by-side player comparison.
- Modular, extensible codebase suitable for experimentation, analysis, and further development.

---

## Tech Stack

**Programming Language**
- Python

**Machine Learning**
- XGBoost  
- Scikit-learn  

**Data Processing**
- Pandas  
- NumPy  
- soccerdata (FBref data extraction)  

**Visualization & Frontend**
- Streamlit  
- Matplotlib  

**Supporting Tools**
- Jupyter Notebook  
- Virtual environment support  
- Requirements-based dependency installation  

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Anurag-Palakurti/premier-league-predictor
cd premier-league-predictor
