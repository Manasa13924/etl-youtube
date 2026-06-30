# etl-youtube
# YouTube Trend ETL & AI Analysis Dashboard 

An end-to-end data engineering and predictive machine learning system that analyzes historical YouTube trending data and integrates live generative AI to assist content creators with automated strategy optimization.

 Key Features
Automated ETL Pipeline: Cleans, deduplicates, and processes historical records using Pandas, storing them in a local warehouse.
Predictive ML Analytics:
*XGBoost Classifier:** Predicts video trending probability with high accuracy ($91.4\%$).
Random Forest Regressor:** Forecasts raw numerical view counts using interactive frontend sliders.
Prescriptive Gen-AI Engine:** Pulls real-time metadata streams via the **YouTube Data API v3** and feeds them into the cloud-hosted **Google Gemini API** to generate high-converting video scripts and strategic channel alignment scores.
- **Interactive UI:** A multi-tab dashboard built on **Streamlit** for zero-latency local operations.

---

 Tech Stack
- **Language:** Python
- **Frontend UI:** Streamlit
- **Data Engineering:** Pandas, SQLite3
- **Machine Learning:** XGBoost, Scikit-Learn (Random Forest)
- **Model Deployment:** Pickle
- **External Cloud APIs:** YouTube Data API v3, Google Gemini API

---

 Core Machine Learning Hyperparameters

 XGBoost Classifier (Trend Prediction)
- `learning_rate`: 0.1
- `n_estimators`: 150
- `max_depth`: 5
- `objective`: binary:logistic

 Random Forest Regressor (View Forecasting)
- `n_estimators`: 100
- `max_depth`: Default / Optimized
- `random_state`: 42
