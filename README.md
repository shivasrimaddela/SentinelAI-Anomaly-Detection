# SentinelAI – Real-Time Anomaly Detection System

SentinelAI is a real-time cybersecurity anomaly detection system designed for monitoring network and application logs.  
It combines **machine learning–based anomaly detection** with **rule-based security analysis** and provides a **live dashboard** to visualize logs, alerts, and detection metrics.

This project demonstrates how modern security monitoring systems identify abnormal behavior using both statistical learning techniques and known attack signatures.

---

## Key Features

- Real-time log generation (normal and malicious traffic)
- Machine learning–based anomaly detection using Isolation Forest and TF-IDF
- Rule-based detection for known cyber attack patterns
- Live alert generation and detection statistics
- Flask-based backend REST API
- React-based interactive frontend dashboard
- Server-Sent Events (SSE) for real-time updates

---

## Detection Approach (Hybrid Model)

SentinelAI follows a **hybrid detection strategy** to improve reliability and coverage.

### 1. Machine Learning–Based Detection
- Trained only on clean, normal traffic
- Learns baseline system behavior
- Detects statistically rare or unusual events

### 2. Rule-Based Detection
- Detects known attack patterns such as:
  - Port scanning
  - Brute-force attempts
  - Unauthorized access
  - Exploit attempts
- Ensures deterministic detection of known threats

**Final anomaly decision = Machine Learning detection OR Rule-based detection**

This hybrid approach enables detection of both **zero-day anomalies** and **known security threats**.

---

## Project Structure

```text
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
│   │   └── realtime_tail_processor.py # Real-time detection engine
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
│   └── generate_logs.py               # Normal and anomaly log generator
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/api.js
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
│
├── notebooks/                         # Optional notebooks for experimentation
├── .gitignore
└── README.md
