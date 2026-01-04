SentinelAI – Real-Time Anomaly Detection System

SentinelAI is a real-time cybersecurity anomaly detection system designed for monitoring network and application logs.
It combines Machine Learning (Isolation Forest) with rule-based security detection and provides a live dashboard to visualize logs, alerts, and detection metrics.

This project demonstrates how modern security systems detect abnormal behavior using both statistical learning techniques and known attack signatures.

Key Features

Real-time log generation (normal and malicious traffic)

Machine Learning–based anomaly detection using Isolation Forest and TF-IDF

Rule-based detection for known cybersecurity attack patterns

Live alerts and detection statistics

Flask-based backend REST API

React-based interactive dashboard

Server-Sent Events (SSE) for real-time updates

Detection Approach (Hybrid Model)

SentinelAI uses a hybrid detection strategy that combines unsupervised machine learning with rule-based logic.

1. Machine Learning Detection

Learns baseline (normal) behavior from clean training logs

Identifies statistically rare or abnormal events

2. Rule-Based Detection

Detects known attack patterns such as:

Port scanning

Brute-force attempts

Unauthorized access

Exploit attempts

Final detection decision:
An event is flagged as an anomaly if either machine learning detection or rule-based detection identifies it as suspicious.

This approach ensures both zero-day anomaly detection and reliable detection of known threats.

Project Structure
SentinelAI/
├── backend/
│   ├── data/
│   │   ├── sample_training_logs.txt   # Normal logs only (training data)
│   │   ├── realtime_logs.txt          # Live generated logs
│   │   └── alerts.log                 # Detected anomalies
│   │
│   ├── models/
│   │   ├── isoforest_model.joblib
│   │   └── tfidf_vectorizer.joblib
│   │
│   ├── scripts/
│   │   ├── train_model.py             # Model training script
│   │   └── realtime_tail_processor.py # Real-time anomaly detection
│   │
│   ├── src/
│   │   ├── app.py                     # Flask application entry point
│   │   ├── config.py                  # Configuration and paths
│   │   ├── utils.py                   # Log preprocessing utilities
│   │   ├── models/
│   │   │   └── anomaly_detector.py
│   │   ├── routes/
│   │   │   ├── logs.py
│   │   │   ├── alerts.py
│   │   │   └── stream.py
│   │   └── services/
│   │       ├── alert_service.py
│   │       └── streaming_service.py
│   │
│   └── generate_logs.py               # Log generator (normal + anomalies)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/api.js
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
│
├── notebooks/                         # Optional notebooks for experiments/EDA
├── .gitignore
└── README.md

File Responsibilities (Overview)
Backend

generate_logs.py
Generates real-time logs that simulate both normal user activity and malicious behavior.

sample_training_logs.txt
Contains only clean, normal logs used to train the machine learning model.

train_model.py
Trains the TF-IDF vectorizer and Isolation Forest model and saves the trained artifacts.

realtime_tail_processor.py
Continuously monitors live logs, applies machine learning and rule-based detection, and records detected anomalies.

anomaly_detector.py
Encapsulates model loading and anomaly prediction logic.

alert_service.py
Stores detected alerts in JSON format and provides alert statistics.

streaming_service.py
Streams live alerts and detection statistics to the frontend using Server-Sent Events.

routes/
Defines Flask API endpoints for logs, alerts, and real-time streaming.

app.py
Main Flask application that initializes and runs the backend API.

Frontend

The frontend dashboard displays:

Total logs processed

Number of detected anomalies

Detection rate

Recent alerts

Live log timeline

The UI updates automatically using backend APIs and SSE.

Execution Steps
1. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

2. Train the Machine Learning Model

Ensure that sample_training_logs.txt contains only normal logs.

cd backend/scripts
python train_model.py

3. Start Log Generation
cd backend
python generate_logs.py

4. Start Real-Time Detection
cd backend/scripts
python realtime_tail_processor.py

5. Start Backend API
cd backend
python -m src.app


Backend will be available at:

http://127.0.0.1:8000

6. Start Frontend
cd frontend
npm install
npm start


Frontend will be available at:

http://localhost:3000

Expected Output

Live logs displayed in the dashboard

Anomalous logs highlighted

Alerts visible in the alerts panel

Detection rate increasing over time

Real-time updates without page refresh

Notes on Training Data

The training dataset must contain only normal behavior.

Do not include the following in training data:

Actions such as scan, exploit, or unauthorized_access

HTTP status codes 401, 403, 404, 500

Including anomalous behavior in training data will prevent the model from detecting anomalies.

Future Enhancements

Attack type classification (scan, brute-force, exploit)

Severity scoring (Low / Medium / High)

Alert acknowledgment and management from the UI

Automatic model retraining

Exporting logs and alerts to CSV

Author Note

This project was developed as a learning and demonstration system for real-time cybersecurity analytics.
It follows industry practices by combining machine learning with rule-based detection to achieve reliable and explainable anomaly detection.

SentinelAI — Intelligent Real-Time Cyber Defense

Status

This repository is ready for academic submission, demonstrations, and portfolio use.
