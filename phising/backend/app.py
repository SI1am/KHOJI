import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from flask import Flask, render_template, request
from flask_cors import CORS
import threading
import joblib
import requests
import pandas as pd
import re
import tldextract
import numpy as np
from scipy.stats import entropy

# FastAPI app
fastapi_app = FastAPI()

MODEL_1_PATH = "phishing.pkl"

try:
    model_1 = joblib.load(MODEL_1_PATH)
except FileNotFoundError:
    raise RuntimeError("Model file phishing.pkl not found!")

@fastapi_app.get("/scan-url")
async def get_scan_url_page():
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

@fastapi_app.post("/predict_model1")
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

def run_fastapi():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)

# Flask app
flask_app = Flask(__name__)
CORS(flask_app)

MODEL_2_PATH = "phishing.pkl"

try:
    model_2 = joblib.load(MODEL_2_PATH)
except FileNotFoundError:
    raise RuntimeError("Model file phishing_detector.pkl not found!")

# **Feature Extraction Function**
def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['num_dashes'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_slashes'] = url.count('/')
    suspicious_keywords = ['login', 'verify', 'secure', 'bank', 'update', 'signin', 'cgi-bin']
    features['has_suspicious_keywords'] = int(any(keyword in url.lower() for keyword in suspicious_keywords))
    features['url_entropy'] = entropy([url.count(char) for char in set(url)], base=2)
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'  
    features['has_ip'] = int(bool(re.search(ip_pattern, url)))
    parsed_url = tldextract.extract(url)
    domain = parsed_url.domain
    features['has_brand_name'] = int(any(brand in domain.lower() for brand in ['google', 'facebook', 'paypal', 'amazon', 'microsoft']))
    features['domain_age'] = np.random.randint(1, 10)
    features['num_redirects'] = np.random.randint(0, 2)
    return features

@flask_app.route("/")
def index():
    return render_template("index.html")

@flask_app.route("/scan", methods=["POST"])
def scan():
    url = request.form.get("url")
    model_choice = request.form.get("model")

    if model_choice == "model1":
        response = requests.post("http://127.0.0.1:8000/predict_model1", json={"url": url})
        result = response.json().get("prediction", "Error connecting to FastAPI backend.")
    elif model_choice == "model2":
        features = pd.DataFrame([extract_features(url)])
        prediction = model_2.predict(features)
        result = "This is a Phishing Site" if prediction[0] == 1 else "This is not a Phishing Site"
    else:
        result = "Invalid model selection."

    return render_template("index.html", url=url, result=result)

def run_flask():
    flask_app.run(debug=False, port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_fastapi).start()
    threading.Thread(target=run_flask).start()
