from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("KAKAO_API_KEY")

pothole_data = []

@app.route('/')
def dashboard():
    """대시보드 HTML 렌더링"""
    return render_template('dashboard.html', api_key=api_key)

@app.route('/api/potholes', methods=['GET'])
def get_potholes():
    """지도 표시용 포트홀 데이터 반환"""
    return jsonify(pothole_data)

@app.route('/api/potholes', methods=['POST'])
def add_pothole():
    """AWS 서버에서 좌표 데이터 수신"""
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
    app.run(debug=True)
