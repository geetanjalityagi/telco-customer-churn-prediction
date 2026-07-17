from fastapi import FastAPI


app = FastAPI(
    title="Predictive Maintenance API",
    version="1.0.0"
)

@app.get('/predict')
def predict():
    return 'Hola'