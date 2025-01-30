from . import db

class CO2Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_km = db.Column(db.Float, default=0)
    bus_km = db.Column(db.Float, default=0)
    energy_kwh = db.Column(db.Float, default=0)
    meat_kg = db.Column(db.Float, default=0)
    veggie_kg = db.Column(db.Float, default=0)
    total_co2 = db.Column(db.Float)