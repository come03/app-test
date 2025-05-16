from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import pandas as pd
import os

app = FastAPI()

class DemandRequest(BaseModel):
    product_name: str
    past_sales: list[int]

HISTORY_FILE = "/Users/comedesolere/demand_forecasting_app/data/history.csv"

# Crée le fichier d'historique s'il n'existe pas
if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["product_name", "past_sales", "forecast"]).to_csv(HISTORY_FILE, index=False)

@app.post("/predict/")
async def predict_demand(request: DemandRequest):
    average_sales = sum(request.past_sales) / len(request.past_sales)
    forecast = round(average_sales * random.uniform(0.8, 1.2), 2)

    # Sauvegarde dans l'historique
    new_row = {"product_name": request.product_name, "past_sales": str(request.past_sales), "forecast": forecast}
    df = pd.read_csv(HISTORY_FILE)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

    return {"product_name": request.product_name, "forecast": forecast}

@app.get("/history/")
async def get_history():
    df = pd.read_csv(HISTORY_FILE)
    return df.to_dict(orient="records")