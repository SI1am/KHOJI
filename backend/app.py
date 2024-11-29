from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import joblib
import pandas as pd
import re
import tldextract
import numpy as np
from scipy.stats import entropy

app = Flask(__name__)
CORS(app)

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    url = request.form.get("url")
    model_choice = request.form.get("model")

    if model_choice == "model1":
        # Call FastAPI's Model 1 prediction endpoint
        response = requests.post("http://127.0.0.1:8000/predict_model1", json={"url": url})
        result = response.json().get("prediction", "Error connecting to FastAPI backend.")
    elif model_choice == "model2":
        # Use Flask's Model 2 directly
        features = pd.DataFrame([extract_features(url)])
        prediction = model_2.predict(features)
        result = "This is a Phishing Site" if prediction[0] == 1 else "This is not a Phishing Site"
    else:
        result = "Invalid model selection."

    return render_template("index.html", url=url, result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
