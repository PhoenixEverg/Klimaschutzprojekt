from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate-co2', methods=['POST'])
def calculate_co2():
    data = request.json
    transport = data.get('transport', 0)  # Kilometer mit Auto
    food = data.get('food', 0)  # CO₂ von Ernährung
    energy = data.get('energy', 0)  # Stromverbrauch
    
    co2_total = (transport * 0.21) + (food * 2.5) + (energy * 0.5)  # Beispielwerte
    return jsonify({'co2_total': co2_total})

if __name__ == '__main__':
    app.run(debug=True)