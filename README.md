# SentinelAI – Real-Time Anomaly Detection System

SentinelAI is a comprehensive **cybersecurity anomaly detection system** that monitors both **application logs** and **network traffic** in real-time. It combines **machine learning-based detection** with **rule-based security analysis** and provides an interactive dashboard to visualize alerts, logs, and detection metrics.

## 🎯 **Key Features**

### **Log-Based Anomaly Detection**
- Real-time log generation (normal and malicious traffic)
- ML-based anomaly detection using Isolation Forest + TF-IDF
- Rule-based detection for attack patterns (port scanning, brute-force, exploitation)
- Live alert generation and statistics

### **Network Anomaly Detection (NEW!)**
- Wireshark packet capture analysis (XLS/XLSX format)
- Network session aggregation and feature extraction
- ML-based detection using Isolation Forest on network features
- Rule-based threat detection for network patterns
- DDoS detection, port scanning detection, suspicious port alerts
- Multi-level severity classification (HIGH/MEDIUM/LOW)

### **Dashboard & API**
- React-based interactive dashboard with real-time updates
- Flask REST API with SSE streaming
- Responsive design (desktop, tablet, mobile)
- Live stats, alerts panel, detailed logs table

---

## 🏗️ **Architecture**

### **Hybrid Detection Strategy**
SentinelAI uses a **two-tier hybrid approach** for maximum threat coverage:

1. **Machine Learning Detection**
   - Isolation Forest: Detects statistical anomalies
   - Works on normalized log/network features
   - Catches zero-day and unusual behavior patterns

2. **Rule-Based Detection**
   - Known attack signatures and threat patterns
   - Deterministic checks for high-confidence threats
   - Assigns severity levels based on threat type

**Final Decision:** Alert triggered if **ML detection OR Rule-based detection** flags activity

---

## 📁 **Project Structure**

```
SentinelAI/
├── backend/
│   ├── data/
│   │   ├── sample_training_logs.txt          # Normal logs (training)
│   │   ├── realtime_logs.txt                 # Live generated logs
│   │   ├── wireshark_sessions.json           # Network sessions (generated)
│   │   ├── wireshark_features.npy            # ML features (generated)
│   │   └── wire shark sample dataset.xls     # Source Wireshark capture
│   │
│   ├── models/
│   │   ├── isoforest_model.joblib            # Log anomaly model
│   │   ├── tfidf_vectorizer.joblib           # Log feature vectorizer
│   │   ├── network_isolation_model.joblib    # Network anomaly model (NEW)
│   │   ├── network_scaler.joblib             # Network feature scaler (NEW)
│   │   └── protocols.joblib                  # Protocol encoder
│   │
│   ├── scripts/
│   │   ├── train_model.py                    # Train log anomaly model
│   │   ├── realtime_tail_processor.py        # Real-time log detection
│   │   ├── wireshark_preprocessor.py         # Convert XLS → JSON sessions (NEW)
│   │   ├── wireshark_feature_extractor.py    # Extract ML features (NEW)
│   │   ├── retrain_wireshark_model.py        # Train network model (NEW)
│   │   └── realtime_tail_processor_network.py # Network detection (NEW)
│   │
│   ├── src/
│   │   ├── app.py                            # Flask app entry point
│   │   ├── config.py                         # Configuration & paths
│   │   ├── utils.py                          # Log utilities
│   │   │
│   │   ├── models/
│   │   │   ├── anomaly_detector.py           # Log ML detector
│   │   │   └── network_anomaly_detector.py   # Network ML detector (NEW)
│   │   │
│   │   ├── routes/
│   │   │   ├── logs.py                       # GET /api/logs
│   │   │   ├── alerts.py                     # GET /api/alerts
│   │   │   └── stream.py                     # Server-Sent Events
│   │   │
│   │   └── services/
│   │       ├── alert_service.py              # Alert logging & parsing
│   │       ├── streaming_service.py          # SSE management
│   │       └── network_rule_engine.py        # Network rule detection (NEW)
│   │
│   ├── requirements.txt                      # Python dependencies
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js                  # Main dashboard
│   │   │   ├── Header.js                     # Top header with stats
│   │   │   ├── StatsCards.js                 # KPI cards
│   │   │   ├── AlertsPanel.js                # Real-time alerts
│   │   │   ├── LogsTable.js                  # Logs table view
│   │   │   ├── Navbar.js                     # Navigation
│   │   │   └── Loader.js                     # Loading spinner
│   │   │
│   │   ├── services/
│   │   │   └── api.js                        # API client
│   │   │
│   │   ├── App.js                            # Main React component
│   │   ├── App.css                           # Original styles
│   │   ├── App_new.css                       # Modern responsive styles
│   │   ├── index.js                          # React entry point
│   │   └── index.css                         # Global styles
│   │
│   ├── package.json                          # NPM dependencies
│   └── public/                                # Static files
│
├── notebooks/
│   └── model_experiments.ipynb                # Experimentation notebook
│
└── README.md                                  # This file
```

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js 14+
- pip and npm

### **Backend Setup**

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Flask server:**
   ```bash
   python -m src.app
   ```
   Server runs at `http://localhost:5000`

### **Frontend Setup**

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install npm packages:**
   ```bash
   npm install
   ```

3. **Start React app:**
   ```bash
   npm start
   ```
   Dashboard opens at `http://localhost:3000`

---

## 🏃 **Execution Steps (Complete Workflow)**

### **PART A: Initial Setup (One-time)**

#### **Step 0: Prerequisites**
Verify you have Python 3.8+ and Node.js 14+:
```bash
python --version
node --version
npm --version
```

---

#### **Step 1: Set Up Backend**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# OR activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

✅ **Expected:** You should see `flask`, `scikit-learn`, `pandas`, `numpy`, `joblib` installed

---

#### **Step 2: Set Up Frontend**

```bash
# Navigate to frontend (open NEW terminal)
cd frontend

# Install npm packages
npm install

# Verify installation
npm list react flask-cors
```

✅ **Expected:** `node_modules` folder created with all dependencies

---

### **PART B: Run Log-Based Detection**

Open **THREE** terminals and run these in order:

#### **Terminal 1: Start Backend Server**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m src.app
```
✅ **Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

---

#### **Terminal 2: Start Frontend Dashboard**
```bash
cd frontend
npm start
```
✅ **Expected Output:**
```
Compiled successfully!
On Your Network: http://192.168.x.x:3000
```
🌐 **Browser opens automatically at http://localhost:3000**

---

#### **Terminal 3: Run Real-Time Log Detection**

**First, train the model (one-time):**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python scripts/train_model.py
```

✅ **Expected Output:**
```
🤖 Training Isolation Forest...
✓ Training complete
📊 Model Performance:
   Accuracy: XX%
   Anomalies found: X
💾 Saved model to backend/models/isoforest_model.joblib
```

---

**Then, start real-time detection:**
```bash
cd backend
python scripts/realtime_tail_processor.py
```

✅ **Expected Output:**
```
🚀 Starting Real-Time Anomaly Detection...
✓ Model loaded
📊 Processing realtime_logs.txt...
⚠️  ANOMALY [1] [HIGH]: ...alert details...
⚠️  ANOMALY [2] [MEDIUM]: ...alert details...
```

🎯 **Watch your dashboard update in real-time!**

---

### **PART C: Run Network Anomaly Detection (NEW!)**

#### **Step 1: Preprocess Wireshark Data**
```bash
cd backend
source venv/bin/activate
python scripts/wireshark_preprocessor.py
```

✅ **Expected Output:**
```
📖 Reading Wireshark file: backend/data/wire shark sample dataset.xls
✓ Read as CSV - Loaded XXX packets
🔄 Aggregating XXX packets into sessions...
✓ Created XXX sessions
🧹 Cleaning sessions...
✓ After cleaning: XXX sessions
💾 Saved XXX sessions to backend/data/wireshark_sessions.json
✅ Preprocessing complete!
```

---

#### **Step 2: Extract Network Features**
```bash
cd backend
python scripts/wireshark_feature_extractor.py
```

✅ **Expected Output:**
```
📖 Loading sessions from backend/data/wireshark_sessions.json
✓ Loaded XXX sessions
🔧 Extracting features from XXX sessions...
✓ Extracted XXX feature vectors
📊 Normalizing XXX feature vectors...
✓ Normalized features
💾 Saved features to backend/data/wireshark_features.npy
💾 Saved scaler to backend/models/network_scaler.joblib
✅ Feature extraction complete!
```

---

#### **Step 3: Train Network Model**
```bash
cd backend
python scripts/retrain_wireshark_model.py
```

✅ **Expected Output:**
```
📖 Loaded XXX feature vectors
🤖 Training Isolation Forest on XXX samples...
✓ Training complete
📊 Model Predictions:
   Normal samples: XXX
   Anomaly samples: XXX
   Anomaly ratio: XX.XX%
💾 Saved model to backend/models/network_isolation_model.joblib
✅ Model retraining complete!
```

---

#### **Step 4: Run Network Real-Time Detection**
```bash
cd backend
python scripts/realtime_tail_processor_network.py
```

✅ **Expected Output:**
```
🚀 Starting Network Anomaly Detection Processor...
📊 Processing XXX sessions...
⚠️  ANOMALY [1] [HIGH]: 192.168.1.100:5432 → 10.0.0.50:3389 [TCP] - Connection to high-risk port...
⚠️  ANOMALY [2] [MEDIUM]: 172.16.0.25:8080 → 8.8.8.8:53 [UDP] - Moderate packet rate...

✅ Processing complete!
   Total sessions: XXX
   Anomalies detected: XX
   Detection rate: XX.XX%
```

---

## 📊 **Usage Guide**

### **Log-Based Detection (Original)**

1. **Generate training logs:**
   ```bash
   python backend/scripts/train_model.py
   ```
   This trains the Isolation Forest on normal logs.

2. **Run real-time detection:**
   ```bash
   python backend/scripts/realtime_tail_processor.py
   ```
   Continuously monitors `realtime_logs.txt` and detects anomalies.

3. **View dashboard:**
   Open `http://localhost:3000` to see real-time alerts and logs.

---

### **Network Detection (NEW!)**

#### **Step 1: Preprocess Wireshark Data**
```bash
python backend/scripts/wireshark_preprocessor.py
```
**Input:** `backend/data/wire shark sample dataset.xls`  
**Output:** `backend/data/wireshark_sessions.json` (aggregated network sessions)

#### **Step 2: Extract Features**
```bash
python backend/scripts/wireshark_feature_extractor.py
```
**Output:** 
- `backend/data/wireshark_features.npy` (normalized features)
- `backend/models/network_scaler.joblib` (feature scaler)

#### **Step 3: Train Network Model**
```bash
python backend/scripts/retrain_wireshark_model.py
```
**Output:** `backend/models/network_isolation_model.joblib` (trained model)

#### **Step 4: Real-Time Network Detection**
```bash
python backend/scripts/realtime_tail_processor_network.py
```
Processes network sessions and logs anomalies with severity levels.

---

## 🔍 **Detection Methods Explained**

### **LOG DETECTION**

| Feature | Source | Model |
|---------|--------|-------|
| Log text embedding | TF-IDF vectorization | Isolation Forest |
| Anomaly score | Decision function | ML model |
| Rule checks | Known patterns | Deterministic rules |

### **NETWORK DETECTION**

| Feature | Computation | Model |
|---------|------------|-------|
| Packet count | From session data | Isolation Forest (8 features) |
| Avg packet size | bytes/packets | Part of ML features |
| Protocol | Numeric encoding | Feature: 1-7 |
| Duration | Time range | Feature |
| Retransmission ratio | retrans/packets | Feature |
| Port suspicion | Port analysis | Feature: 0-1 flag |
| Packet rate | packets/second | Feature |
| High risk ports | Windows services | Rule-based: HIGH severity |

### **Rule Examples (Network)**

- **DDoS Detection:** Packet rate > 500 packets/sec → **HIGH severity**
- **Port Scanning:** Source connecting to >20 different ports → **HIGH**
- **Retransmission Spike:** >50% retransmissions → **HIGH**
- **Suspicious Ports:** Connection to RDP (3389), SMB (445) → **HIGH**
- **Unusual Activity:** Moderate packet rate 100-200 → **MEDIUM**

---

## 🛠️ **API Endpoints**

### **GET /api/logs**
Fetch recent logs with optional filters
```bash
curl http://localhost:5000/api/logs?limit=50
```

### **GET /api/alerts**
Get detected anomalies
```bash
curl http://localhost:5000/api/alerts?severity=HIGH
```

### **GET /api/stream**
Server-Sent Events for real-time updates
```bash
curl -N http://localhost:5000/api/stream
```

---

## 📦 **Technologies Used**

**Backend:**
- Flask 2.3+ (REST API)
- scikit-learn (ML models)
- pandas, numpy (Data processing)
- joblib (Model serialization)
- python-dotenv (Configuration)

**Frontend:**
- React 18+
- CSS3 (Responsive design)
- Fetch API (HTTP requests)
- Server-Sent Events (Real-time updates)

**Data:**
- Wireshark packet captures (XLS/XLSX)
- Pandas for data manipulation
- NumPy for feature arrays

---

## 🔐 **Severity Levels**

| Level | Color | When Triggered |
|-------|-------|----------------|
| **HIGH** | 🔴 Red | Critical threats, RDP/SMB access, DDoS patterns, severe retransmissions |
| **MEDIUM** | 🟠 Orange | Suspicious patterns, unusual ports, moderate packet rates |
| **LOW** | 🟢 Green | Minor issues, non-standard ports, informational alerts |

---

## 📝 **Configuration**

Edit `backend/src/config.py` to customize:
- Flask host/port
- Model paths
- Data directory locations
- CORS origins
- Log file paths

---

## 🤝 **Contributing**

Contributions welcome! Please:
1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

---

## 📄 **License**

MIT License - Feel free to use for learning and research.

---

## 📧 **Support**

For issues or questions, open a GitHub issue or contact the development team.

---

**Last Updated:** April 2026  
**Version:** 2.0 (With Network Anomaly Detection)
