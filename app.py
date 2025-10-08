from flask import Flask, render_template, jsonify
import random, time

app = Flask(__name__)

data_history = []

def generate_data():
    current = round(random.uniform(0.2, 2.0), 2)
    voltage = 220
    power = round(current * voltage, 2)
    predicted = round(power * random.uniform(0.95, 1.05), 2)
    return {"current": current, "voltage": voltage, "power": power, "predicted": predicted}

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    # simulate new reading every time the browser requests data
    latest_data = generate_data()
    data_history.append(latest_data["power"])
    if len(data_history) > 30:
        data_history.pop(0)
    avg_power = round(sum(data_history) / len(data_history), 2) if data_history else 0
    return jsonify({
        "latest": latest_data,
        "history": data_history,
        "avg_power": avg_power
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
