import requests
import random
import time

url = "http://127.0.0.1:5000/webhook"

for i in range(20): 
    data = {
        "transaction_id": f"TX{i+1}",
        "amount": random.randint(1000, 100000),
        "type": random.choice(["buy", "sell"]),
        "risk_score": random.randint(0, 100)
    }
    response = requests.post(url, json=data)
    print(response.json())
    time.sleep(2)  
