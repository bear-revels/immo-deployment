from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from api.predict import predict_price, load_preprocessing_steps, apply_preprocessing

# Define input data schema
class InputData(BaseModel):
    PostalCode: int
    Province: str
    PropertySubType: str
    BedroomCount: int
    LivingArea: float
    KitchenType: str
    Furnished: int
    Fireplace: int
    TerraceArea: float
    GardenArea: float
    Facades: int
    SwimmingPool: int
    EnergyConsumptionPerSqm: float
    Condition: str
    Latitude: float
    Longitude: float

# Define FastAPI app
app = FastAPI()

# Define API endpoint for predicting property prices
@app.post("/predict/")
def predict_property_price(data: InputData):
    input_df = pd.DataFrame([data.dict()])

    # Load preprocessing steps
    preprocessing_steps = load_preprocessing_steps("./preprocessing_steps.json")

    # Apply preprocessing steps
    preprocessed_data = apply_preprocessing(input_df, preprocessing_steps)

    # Make predictions using the loaded model
    prediction = predict_price(preprocessed_data)

    return {"prediction": round(float(prediction), 2), "status_code": 200}