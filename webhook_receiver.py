import json
from flask import Flask, request, jsonify
from datetime import datetime
import threading
import random
import time

app = Flask(__name__)
FILE = "transactions.json"
lock = threading.Lock()  
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Add timestamp
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Received data:", data)

   
    with lock:
        try:
            with open(FILE, "r") as f:
                all_tx = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_tx = []

        all_tx.append(data)
        with open(FILE, "w") as f:
            json.dump(all_tx, f, indent=4)

    # Alert high-risk
    if data.get("risk_score", 0) >= 70:
        print("⚠️ High-risk transaction detected!")

    return jsonify({"status": "received", "risk_score": data.get("risk_score", 0)})


def simulate_transactions():
    while True:
        data = {
            "transaction_id": f"TX{random.randint(1000,9999)}",
            "amount": random.randint(1000, 100000),
            "type": random.choice(["buy", "sell"]),
            "risk_score": random.randint(0, 100)
        }
       
        try:
            import requests
            requests.post("http://127.0.0.1:5000/webhook", json=data)
        except Exception as e:
            print("Simulator error:", e)
        time.sleep(2)  

if __name__ == "__main__":
    threading.Thread(target=simulate_transactions, daemon=True).start()
    app.run(port=5000, debug=True)
