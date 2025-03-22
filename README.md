KHOJI - Ransomware Detection System
A web-based application to scan files for potential ransomware. This system calculates the Shannon entropy of uploaded files and uses a trained machine learning model to classify them as either safe or ransomware.

Features
📂 File Scanning: Upload a file to scan for ransomware.
🔍 Entropy Analysis: Calculates Shannon entropy to detect encryption patterns.
🤖 Machine Learning: Uses a trained Random Forest model for classification.
🛡️ Mitigation Steps: Provides logs and suggested actions if ransomware is detected.
🖥️ Web Interface: User-friendly interface for file uploads and scan results.
Installation
Clone the repository:
git clone https://github.com/your-username/ransomware-detection-system.git
cd ransomware-detection-system
2️⃣ Create and activate a virtual environment python -m venv venv source venv/bin/activate # Linux/Mac venv\Scripts\activate # Windows

3️⃣ Install dependencies pip install -r requirements.txt

5️⃣ Start the Flask application python app.py

6️⃣ Open the application Open your browser and visit: http://127.0.0.1:5000/

**Project Structure **:- ransomware-detection-system/ ├── app.py # Main application script ├── ml_model/ │ └── ransomware_detector.pkl # Trained ML model ├── templates/ │ └── index.html # Frontend template ├── uploads/ # Directory for uploaded files (auto-created) ├── requirements.txt # Python dependencies └── README.md # Project documentation

Usage Follow these steps to scan a file:

1️⃣ Navigate to the homepage in your browser: http://127.0.0.1:5000/ 2️⃣ Upload a file using the "Choose File" button.

3️⃣ Click the "Scan" button to analyze the file.

4️⃣ View the results:

Ransomware Detected: Displays logs, entropy value, and suggested mitigation steps. Safe: Indicates the file is not ransomware.

Dependencies The project requires the following dependencies:

Python 3.8 or higher Flask Joblib Scikit-learn Math library (built-in) Install all dependencies.

Training the ML Model If the ransomware_detector.pkl file is missing, you can train the model with the following steps:

1️⃣ Create or use an existing dataset Generate or use a dataset containing entropy values and their respective labels (1 for ransomware, 0 for safe files).

2️⃣ Use the following script to train the model: import pandas as pd from sklearn.ensemble import RandomForestClassifier from sklearn.model_selection import train_test_split import joblib

Example dataset
data = { "entropy": [4.2, 5.7, 6.3, 1.8, 2.3, 7.1], "label": [1, 1, 1, 0, 0, 1] # 1 = Ransomware, 0 = Safe } df = pd.DataFrame(data)

X = df[["entropy"]] y = df["label"]

Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) model = RandomForestClassifier(n_estimators=100, random_state=42) model.fit(X_train, y_train)

Save model
joblib.dump(model, "ml_model/ransomware_detector.pkl") print("Model trained and saved.")

3️⃣ Save the model Save the trained model as ransomware_detector.pkl inside the ml_model directory.

Contributing Contributions are welcome! Follow these steps to contribute:

1️⃣ Fork the repository.

2️⃣ Create a new branch: git checkout -b feature-name

3️⃣ Commit your changes: git commit -m "Description of changes" 4️⃣ Push to the branch: git push origin feature-name 5️⃣ Open a pull request on GitHub.

License This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments Inspired by real-world ransomware detection needs. Thanks to the open-source community for their contributions!

This format provides a step-by-step guide for each section, with clean and easy-to-follow instructions. Let me know if you'd like to adjust or add more sections!
