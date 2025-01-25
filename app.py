from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate-co2', methods=['POST'])
def calculate_co2():
    data = request.json
    transport = data.get('transport', 0)  # type: ignore # Kilometer mit Auto
    food = data.get('food', 0)  # type: ignore # CO₂ von Ernährung
    energy = data.get('energy', 0)  # type: ignore # Stromverbrauch
    
    co2_total = (transport * 0.21) + (food * 2.5) + (energy * 0.5)  # Beispielwerte
    return jsonify({'co2_total': co2_total})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)