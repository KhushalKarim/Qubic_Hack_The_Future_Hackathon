# Qubic_Hack_The_Future_Hackathon

QubicGuard – AI-based Risk Monitoring for Qubic Transactions

**Project Overview**
QubicGuard is a live dashboard that monitors blockchain transactions in real-time, identifies high-risk activities, and provides interactive visualizations. It uses a Flask webhook to receive transaction data and a Streamlit dashboard for live analytics.

**Features**
1. Live Transaction Monitoring: Streams transactions in real-time from a simulator or webhook.
2. High-Risk Alerts: Highlights transactions with risk_score ≥ 70.
3. Interactive Dashboard: Shows recent transactions, charts for transaction amounts, and high-risk alerts.
4. Simulator Included: Generates sample transactions for testing the pipeline.

**Technologies**
1. Python
2. Flask – Webhook receiver
3. Streamlit – Interactive dashboard
4. Pandas – Data processing
5. Requests – Sending simulated webhook data

**Setup & Run**
Create environment (Python 3.9 recommended):
conda create -n qubicguard python=3.9
conda activate qubicguard

**Install dependencies**
pip install flask streamlit pandas requests
Run Webhook Receiver with Simulator:
python webhook_receiver.py

**Open Dashboard in a new terminal**
streamlit run dashboard.py

**View live dashboard**
URL: Streamlit (usually http://localhost:8501)

**Demo**
Transactions appear live on the dashboard.
High-risk transactions are highlighted automatically.
Charts and metrics refresh every 5 seconds.

**Project Structure**
qubicguard/
│
├─ webhook_receiver.py   This is Flask webhook + simulator
├─ dashboard.py          This is  Streamlit live dashboard
├─ transactions.json     This is JSON file storing transaction data
├─ test_send.py          This is  Optional webhook testing script
└─ data/                 This Optional folder for extra data files
