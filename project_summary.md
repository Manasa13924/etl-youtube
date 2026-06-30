# YouTube ETL & AI Analytics Dashboard - Project Summary

This project is a comprehensive data pipeline and dashboard for analyzing YouTube trending videos. It extracts data from the YouTube Data API and local CSV files, transforms the data to engineer new features, loads it into a SQLite database, trains machine learning models on the data, and visualizes the insights using an interactive Streamlit dashboard.

## Project Structure

- `main.py`: The main Streamlit dashboard application.
- `scripts/etl.py`: The ETL pipeline script (Extract, Transform, Load).
- `scripts/models.py`: The script to train the sentiment analysis and view prediction models.
- `scripts/scheduler.py`: A scheduler script to run the ETL process automatically every 24 hours.
- `tests/test_etl.py`: Unit tests for the ETL process.
- `data/`: Directory containing the local dataset (`INvideos.csv`, `IN_category_id.json`) and the generated SQLite database (`trends.db`).
- `models/`: Directory where the trained models are saved.

## Setup Requirements

Before running any scripts, ensure you have the required packages installed. 
You will need packages like `pandas`, `numpy`, `streamlit`, `google-api-python-client`, `scikit-learn`, `sqlite3`, `python-dotenv`, `plotly`, `schedule`, and `pytest`.

To install the dependencies required for the scheduler and testing, run:
```bash
pip install schedule pytest
```

Make sure you have a `.env` file in the root directory containing your YouTube API key:
```env
YOUTUBE_API_KEY=your_api_key_here
```

## How to Run Each Component

### 1. ETL Pipeline (Manual Run)
To manually run the ETL process and populate your database with fresh data:
```bash
python scripts/etl.py
```

### 2. Model Training
To train or re-train the AI models (Sentiment Classifier and View Predictor) on the latest database records:
```bash
python scripts/models.py
```
This will save the trained models in the `models/` directory.

### 3. Streamlit Dashboard
To launch the interactive dashboard to visualize the data and use the AI predictor:
```bash
streamlit run main.py
```

### 4. Automated Scheduler
To keep your data continuously updated, you can run the scheduler script in the background. It is configured to run the ETL process every 24 hours.
```bash
python scripts/scheduler.py
```
Logs for the scheduler will be written to `scheduler.log`.

### 5. Running Tests
To ensure the ETL pipeline logic is functioning correctly, you can run the test suite using `pytest`:
```bash
pytest tests/
```
