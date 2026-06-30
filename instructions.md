# Project: YouTube Trend ETL & AI Analysis

## Objective
Build a system that takes trending YouTube data (from Kaggle and the Live API), cleans it, and uses AI to predict trends and analyze sentiment.

## Architecture
1. **ETL (scripts/etl.py):** - Load Kaggle CSVs from /data.
   - Fetch live data using YouTube Data API v3.
   - Clean data (remove duplicates, fix dates).
   - Store in a SQLite database.

2. **AI Models (scripts/models.py):**
   - Sentiment Analysis on video titles.
   - View count prediction using Scikit-Learn or TensorFlow.

3. **Dashboard (main.py):**
   - A Streamlit app to show charts of trending categories and AI predictions.

## Constraints
- Use the API key from the .env file.
- Follow the existing folder structure.
- All code must be modular.
