def calculate_co2(data):
    factors = {
        "car": 0.21,   # kg CO₂ pro km (Durchschnittsauto)
        "bus": 0.05,   # kg CO₂ pro km (ÖPNV)
        "bike": 0.00,  # Fahrrad = 0 CO₂
        "energy": 0.45, # kg CO₂ pro kWh
        "meat": 5.0,   # kg CO₂ pro kg Fleisch
        "veggie": 2.0  # kg CO₂ pro kg Gemüse
    }

    transport_co2 = data.get("car", 0) * factors["car"] + data.get("bus", 0) * factors["bus"]
    energy_co2 = data.get("energy", 0) * factors["energy"]
    food_co2 = data.get("meat", 0) * factors["meat"] + data.get("veggie", 0) * factors["veggie"]

    total = transport_co2 + energy_co2 + food_co2

    suggestions = []
    if transport_co2 > 100:
        suggestions.append("Versuche, öfter den Bus oder das Fahrrad zu nutzen.")
    if energy_co2 > 200:
        suggestions.append("Überlege, auf Ökostrom umzusteigen.")
    if food_co2 > 50:
        suggestions.append("Reduziere deinen Fleischkonsum für ein besseren CO₂-Fußabdruck.")

    return {"total_co2": total, "suggestions": suggestions}

def validate_data(data):
    errors = []
    valid_fields = ['car', 'bus', 'energy', 'meat', 'veggie']
    
    if not any(data.get(field, 0) for field in valid_fields):
        errors.append("Mindestens ein Wert muss größer als 0 sein")
    
    return errors