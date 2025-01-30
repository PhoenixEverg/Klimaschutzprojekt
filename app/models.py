from . import db
from datetime import datetime, UTC

class CO2Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    car_km = db.Column(db.Float, default=0)
    bus_km = db.Column(db.Float, default=0)
    energy_kwh = db.Column(db.Float, default=0)
    meat_kg = db.Column(db.Float, default=0)
    veggie_kg = db.Column(db.Float, default=0)
    total_co2 = db.Column(db.Float)