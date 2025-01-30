from flask import Blueprint, request, jsonify
from .models import CO2Entry
from . import db
from .utils import calculate_co2, validate_data

main = Blueprint("main", __name__)

@main.route("/calculate", methods=["POST"])
def calculate():
    data = request.json  
    result = calculate_co2(data)
    errors = validate_data(data)

    new_entry = CO2Entry(
        car_km=data.get("car", 0),
        bus_km=data.get("bus", 0),
        energy_kwh=data.get("energy", 0),
        meat_kg=data.get("meat", 0),
        veggie_kg=data.get("veggie", 0),
        total_co2=result["total_co2"]
    )

    db.session.add(new_entry)
    db.session.commit()

    if errors:
        return jsonify({"errors": errors}), 400  # Fehlerhafte Anfrage

    return jsonify(result)