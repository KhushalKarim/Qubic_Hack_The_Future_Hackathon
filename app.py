import streamlit as st
import pandas as pd
import json
import time
import threading
import random
from datetime import datetime

st.set_page_config(page_title="QubicGuard Dashboard", layout="wide")

FILE = "transactions.json"
lock = threading.Lock()

st.title("🛡️ QubicGuard — Real-Time Risk Monitoring")
st.markdown("Live AI-based risk detection for Qubic network transactions.")

# -----------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------
def load_transactions():
    """Loads JSON transaction history safely."""
    try:
        with open(FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return pd.DataFrame()
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                data = []
                for line in content.splitlines():
                    if line.strip():
                        data.append(json.loads(line))
            return pd.DataFrame(data)
    except FileNotFoundError:
        return pd.DataFrame()

def save_transaction(data):
    """Thread-safe append to JSON file."""
    with lock:
        try:
            with open(FILE, "r") as f:
                all_tx = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_tx = []

        all_tx.append(data)
        with open(FILE, "w") as f:
            json.dump(all_tx, f, indent=4)

# -----------------------------------------------------------
# Simulator (Runs in Background)
# -----------------------------------------------------------
def simulator():
    """Generates fake Qubic transactions every 2 seconds."""
    while True:
        data = {
            "transaction_id": f"TX{random.randint(1000, 9999)}",
            "amount": random.randint(1000, 100000),
            "type": random.choice(["buy", "sell"]),
            "risk_score": random.randint(0, 100),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_transaction(data)
        time.sleep(2)

# Start simulator thread only once
if "sim_started" not in st.session_state:
    threading.Thread(target=simulator, daemon=True).start()
    st.session_state.sim_started = True

# -----------------------------------------------------------
# Dashboard UI
# -----------------------------------------------------------
placeholder = st.empty()

while True:
    df = load_transactions()

    with placeholder.container():
        if not df.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Transactions", len(df))
            col2.metric("High-Risk Transactions", len(df[df["risk_score"] >= 70]))
            col3.metric("Avg Amount", f"${df['amount'].mean():,.2f}")

            st.subheader("📄 Recent Transactions")
            def highlight_risk(row):
                return ['background-color: #FFCCCC' if row.risk_score >= 70 else '' for _ in row]

            st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True)

            st.subheader("📊 Transaction Amounts")
            st.bar_chart(df["amount"])

            st.subheader("📈 Risk Score Distribution")
            st.bar_chart(df["risk_score"])
        else:
            st.info("Waiting for transactions...")

    time.sleep(3)
