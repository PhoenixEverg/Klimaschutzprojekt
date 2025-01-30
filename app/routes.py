from flask import Blueprint, request, jsonify
from .models import CO2Entry
from . import db
from .utils import calculate_co2, validate_data

main = Blueprint("main", __name__)

@main.route("/calculate", methods=["POST"])
def calculate():
    data = request.json  
    errors = validate_data(data)

    if errors:
        return jsonify({"errors": errors}), 400

    result = calculate_co2(data)

    new_entry = CO2Entry(
        car_km=data.get("car", 0), # type: ignore
        bus_km=data.get("bus", 0), # type: ignore
        energy_kwh=data.get("energy", 0), # type: ignore
        meat_kg=data.get("meat", 0), # type: ignore
        veggie_kg=data.get("veggie", 0), # type: ignore
        total_co2=result["total_co2"] # type: ignore
    )

    db.session.add(new_entry)
    db.session.commit()

    return jsonify(result)