from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your Elastic Beanstalk API URL
ELASTIC_BEANSTALK_URL = "http://alzheimer-env.eba-yqcjrnts.us-west-2.elasticbeanstalk.com/predict"

@app.route("/")
def home():
    return jsonify({
        "message": "CORS Proxy for Alzheimer Prediction API",
        "target_url": ELASTIC_BEANSTALK_URL,
        "usage": "POST to /predict with JSON data"
    })

@app.route("/predict", methods=["POST", "OPTIONS"])
def proxy_predict():
    if request.method == "OPTIONS":
        # Handle preflight request
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    
    try:
        # Get data from frontend
        data = request.get_json()
        
        # Forward request to Elastic Beanstalk
        response = requests.post(
            ELASTIC_BEANSTALK_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Return the response from Elastic Beanstalk
        result = response.json()
        
        if response.status_code == 200:
            return jsonify(result)
        else:
            return jsonify(result), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Connection to API failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Proxy error: {str(e)}"}), 500

if __name__ == "__main__":
    print("🚀 CORS Proxy Server starting...")
    print("🌐 Frontend can now call: http://localhost:5000/predict")
    print("📡 Proxy forwards to:", ELASTIC_BEANSTALK_URL)
    app.run(host="0.0.0.0", port=5000, debug=True)