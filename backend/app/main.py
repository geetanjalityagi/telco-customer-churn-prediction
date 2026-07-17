from fastapi import FastAPI


app = FastAPI(
    title="Customer Churn API",
    version="1.0.0"
)

@app.get('/predict')
def predict():
    return 'Hola'