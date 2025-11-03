from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

api_key = os.getenv("KAKAO_API_KEY")

pothole_data = []

@app.route('/')
def dashboard():
    return render_template('dashboard.html', api_key=api_key)

@app.route('/api/potholes', methods=['GET'])
def get_potholes():
    return jsonify(pothole_data)

@app.route('/api/potholes', methods=['POST'])
def add_pothole():
    data = request.get_json()

    pothole_entry = {
        "id": data.get("id", f"pothole_{len(pothole_data)+1}"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "severity": data.get("severity", "Unknown"),
        "timestamp": data.get("timestamp", datetime.now().isoformat()),
        "status": data.get("status", "Unresolved"),
        "image_url": data.get("image_url", "")
    }

    pothole_data.append(pothole_entry)
    print(f"[NEW DATA] {pothole_entry}")  

    return jsonify({"message": "Pothole added successfully"}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
