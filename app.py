from flask import Flask, render_template, jsonify
import random, threading, time

app = Flask(__name__)

latest_data = {"current": 0, "voltage": 0, "power": 0}
data_history = []  # store last 30 readings for chart display


def simulate_iot_data():
    global latest_data, data_history
    while True:
        current = round(random.uniform(0.2, 2.0), 2)   # amperes
        voltage = 220
        power = round(current * voltage, 2)

        # simple "AI-ready" prediction model (for demo)
        predicted = round(power * random.uniform(0.95, 1.05), 2)

        latest_data = {
            "current": current,
            "voltage": voltage,
            "power": power,
            "predicted": predicted
        }

        data_history.append(power)
        if len(data_history) > 30:
            data_history.pop(0)

        time.sleep(2)


threading.Thread(target=simulate_iot_data, daemon=True).start()


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/data')
def get_data():
    avg_power = round(sum(data_history) / len(data_history), 2) if data_history else 0
    return jsonify({
        "latest": latest_data,
        "history": data_history,
        "avg_power": avg_power
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
