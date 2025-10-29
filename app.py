from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the optimized XGBoost model
model = joblib.load("xgb_top_features.pkl")
print("New XGBoost version deployed!")


# Define the top 9 features used for prediction
FEATURES = [
    "MemoryComplaints",
    "BehavioralProblems",
    "MMSE",
    "ADL",
    "FunctionalAssessment",
    "Smoking",
    "Disorientation",
    "Age",
    "CholesterolTriglycerides"
]

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Alzheimer Prediction API is running 🚀",
        "required_features": FEATURES
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Ensure all required features are present
        missing = [f for f in FEATURES if f not in data]
        if missing:
            return jsonify({"error": f"Missing features: {missing}"}), 400

        # Create DataFrame for prediction
        input_df = pd.DataFrame([data], columns=FEATURES)

        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = float(model.predict_proba(input_df)[0][1])

        return jsonify({
            "prediction": int(prediction),
            "probability": round(probability, 4)
            "note": "🧠 Model updated via CI/CD!"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
