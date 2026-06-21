from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Customer Risk Prediction API")

# Load model and encoders
model = joblib.load("xgb_model.pkl")


class CustomerData(BaseModel):
    customer_order_count: int
    customer_total_spending: float
    price: float
    freight_value: float

    seller_state: str
    product_category_name: str
    payment_type: str
    customer_state: str

    avg_order_value: float
    seller_order_count: int


@app.get("/")
def home():
    return {"message": "API Running Successfully"}


@app.post("/predict")
def predict(data: CustomerData):

    try:
        df = pd.DataFrame([data.model_dump()])

        # Encode categorical features
        categorical_cols = [
            "seller_state",
            "product_category_name",
            "payment_type",
            "customer_state"
        ]

        for col in categorical_cols:
            df[col] = df[col].astype("category")

        prediction = int(model.predict(df)[0])
        probability = float(model.predict_proba(df)[0][1])

        return {
            "prediction": prediction,
            "risk_probability": round(probability, 4),
            "risk_label": "High Risk" if prediction == 1 else "Low Risk"
        }

    except Exception as e:
        return {"error": str(e)}
    