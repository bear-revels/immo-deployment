from fastapi import FastAPI
import numpy as np
import pandas as pd
from predict import predict_price
from pydantic import BaseModel
from typing import Optional

# Define input data schema
class InputData(BaseModel):
    PostalCode: int
    Region: str
    District: str
    Province: str
    PropertyType: str
    PropertySubType: str
    BedroomCount: int
    LivingArea: float
    KitchenType: Optional[str] 
    Furnished: Optional[int]
    Fireplace: Optional[int]
    Terrace: int
    TerraceArea: Optional[float] 
    Garden: int
    GardenArea: Optional[float] 
    Facades: Optional[int] 
    SwimmingPool: Optional[int]  
    EnergyConsumptionPerSqm: Optional[float]
    Condition: Optional[str]
    EPCScore: Optional[str]
    Latitude: Optional[float] 
    Longitude: Optional[float] 

# Define FastAPI app
app = FastAPI()

# Define root endpoint
@app.get("/")
def read_root():
    return {"message": "It's alive!"}

# Define API endpoint for predicting property prices
@app.post("/predict/")
def predict_property_price(data: InputData):
    input_df = pd.DataFrame([data.dict()])

    # Load preprocessing steps
    predicted_price = predict_price(input_df)

    # Format prediction as currency
    formatted_prediction = f'€{predicted_price:,.2f}'

    return {"prediction": formatted_prediction, "status_code": 200}