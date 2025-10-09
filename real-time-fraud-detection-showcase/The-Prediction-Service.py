# Description:  This snippet shows how we serve our trained model via a fast,
#               reliable, and production-ready API using FastAPI.
# ==============================================================================

from fastapi import FastAPI
from pydantic import BaseModel
# In a real app, you would import joblib or another model loading library.

# This is our FastAPI app. It's the server that will listen for requests.
app = FastAPI(title="Fraud Detection API")

# Pro-tip for production: Load the model *once* when the server starts.
# This avoids the costly operation of reloading the model file from disk
# for every single prediction, which is key for a low-latency system.
# model = joblib.load("fraud_model.joblib")

# Pydantic models are like a bouncer for our API. This class checks every
# incoming request to make sure the data is in the exact format we expect.
# If the data is bad, FastAPI automatically rejects it with a clear error.
class Transaction(BaseModel):
    # In the real project, all required features would be listed here.
    V1: float
    V2: float
    V3: float
    scaled_amount: float
    scaled_time: float

# This is our main endpoint. It's the front door for getting predictions.
# It only listens for POST requests at our /predict URL.
@app.post("/predict")
def predict(transaction: Transaction):
    """
    A client sends transaction data, we feed it to the model, and send
    back a simple "is_fraud" answer.
    """
    # 1. Convert the incoming JSON request into the format the model expects.
    # input_df = pd.DataFrame([transaction.dict()])

    # 2. Use the pre-loaded "brain" to make the actual prediction.
    # prediction = model.predict(input_df)

    # 3. Send back a simple, clean JSON response.
    # In a real system, we'd use a placeholder here since the model isn't loaded.
    is_fraud_prediction = 1 # Placeholder response

    return {"is_fraud": is_fraud_prediction}
