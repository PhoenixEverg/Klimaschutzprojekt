from flask import Blueprint, render_template, request, jsonify
from .utils import calculate_co2

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/calculate", methods=["POST"])
def calculate():
    data = request.json  # JSON-Daten vom Frontend
    result = calculate_co2(data)
    return jsonify(result)