from fastapi import FastAPI, HTTPException
import joblib
from fastapi.responses import HTMLResponse

app = FastAPI()

MODEL_1_PATH = "phishing.pkl"

try:
    model_1 = joblib.load(MODEL_1_PATH)
except FileNotFoundError:
    raise RuntimeError("Model file phishing.pkl not found!")

@app.get("/scan-url")
async def get_scan_url_page():
    """
    Render the page where users can input URL for phishing detection.
    """
    html_content = """
    <html>
        <body>
            <h1>Enter URL to Scan for Phishing</h1>
            <form action="/predict_model1" method="post">
                <input type="text" name="url" placeholder="Enter URL here" required>
                <button type="submit">Scan URL</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/predict_model1")
async def predict_model1(data: dict):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL not provided.")
    try:
        X_predict = [url]
        y_predict = model_1.predict(X_predict)
        result = "This is a Phishing Site" if y_predict[0] == "bad" else "This is not a Phishing Site"
        return {"url": url, "prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
