from flask import Flask, render_template, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

# store latest readings (dummy in-memory database)
data_log = []

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    return jsonify(data_log[-20:])  # send last 20 data points

@app.route('/upload', methods=['POST'])
def upload_data():
    content = request.get_json()
    content['timestamp'] = datetime.now().strftime("%H:%M:%S")
    data_log.append(content)
    if len(data_log) > 100:
        data_log.pop(0)
    return jsonify({"status": "received"})

@app.route('/predict')
def predict_usage():
    if not data_log:
        return jsonify({"predicted_power": 0})
    recent = [d['power'] for d in data_log[-5:]]
    avg_power = sum(recent) / len(recent)
    predicted = round(avg_power * random.uniform(0.9, 1.1), 2)
    return jsonify({"predicted_power": predicted})

if __name__ == '__main__':
    app.run(debug=True)
