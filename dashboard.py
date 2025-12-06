import streamlit as st
import pandas as pd
import json
import time

st.set_page_config(page_title="QubicGuard Dashboard", layout="wide")
st.title("🛡️ QubicGuard Dashboard")
st.markdown("**AI-based Risk Monitoring for Qubic Transactions**")

FILE = "transactions.json"

def load_transactions():
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

# Live dashboard placeholder
placeholder = st.empty()

while True:
    df = load_transactions()

    with placeholder.container():
        if not df.empty:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Transactions", len(df))
            col2.metric("High-Risk Transactions", len(df[df["risk_score"] >= 70]))
            col3.metric("Average Amount", f"${df['amount'].mean():,.2f}")

            st.subheader("Recent Transactions")
            # Highlight high-risk rows
            def highlight_risk(row):
                return ['background-color: #FFCCCC' if row.risk_score >= 70 else '' for _ in row]
            st.dataframe(df.style.apply(highlight_risk, axis=1), use_container_width=True)

           
            st.subheader("Transaction Amounts")
            st.bar_chart(df["amount"])

            
            st.subheader("Risk Score Distribution")
            st.bar_chart(df["risk_score"])
        else:
            st.info("No transactions yet.")

    time.sleep(5)  
