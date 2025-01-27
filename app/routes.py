from flask import Blueprint, request, jsonify
from .utils import calculate_co2

main = Blueprint("main", __name__)

@main.route("/calculate", methods=["POST"])
def calculate():
    data = request.json  # JSON-Daten vom Frontend
    result = calculate_co2(data)
    return jsonify(result)