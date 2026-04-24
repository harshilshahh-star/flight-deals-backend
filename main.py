from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, timedelta
import os

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("KIWI_API_KEY")

@app.get("/")
def home():
    return {"message": "Flight API is running"}

@app.get("/deals")
def get_deals():
    url = "https://api.tequila.kiwi.com/v2/search"

    params = {
        "fly_from": "AMD",
        "fly_to": "anywhere",
        "date_from": datetime.today().strftime("%d/%m/%Y"),
        "date_to": (datetime.today() + timedelta(days=90)).strftime("%d/%m/%Y"),
        "curr": "INR",
        "price_to": 20000,
        "limit": 20,
        "sort": "price"
    }

    headers = {
        "apikey": API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    deals = []

    for f in data.get("data", []):
        deals.append({
            "from": f["cityFrom"],
            "to": f["cityTo"],
            "price": f["price"],
            "date": f["local_departure"][:10],
            "link": f["deep_link"]
        })

    return deals
