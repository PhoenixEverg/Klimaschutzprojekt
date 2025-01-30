from flask import Blueprint, request, jsonify, send_file
from .models import CO2Entry
from . import db
from .utils import calculate_co2, validate_data
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Required for non-interactive backend

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

@main.route("/visualization", methods=["GET"])
def get_visualization():
    entries = CO2Entry.query.all()
    
    data = {
        'car_km': [],
        'bus_km': [],
        'energy_kwh': [],
        'meat_kg': [],
        'veggie_kg': [],
        'total_co2': [],
        'timestamp': []
    }
    
    for entry in entries:
        data['car_km'].append(entry.car_km)
        data['bus_km'].append(entry.bus_km)
        data['energy_kwh'].append(entry.energy_kwh)
        data['meat_kg'].append(entry.meat_kg)
        data['veggie_kg'].append(entry.veggie_kg)
        data['total_co2'].append(entry.total_co2)
        data['timestamp'].append(entry.timestamp)
    
    df = pd.DataFrame(data)
    
    # Ändern Sie den Stil zu 'ggplot' statt 'seaborn'
    plt.style.use('ggplot')
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Total CO2 over time
    ax1.plot(df['timestamp'], df['total_co2'], 
             marker='o', 
             color='#2ecc71', 
             linewidth=2, 
             markersize=8)
    ax1.fill_between(df['timestamp'], df['total_co2'], 
                     alpha=0.2, 
                     color='#2ecc71')
    ax1.set_title('Total CO2 Emissions Over Time', 
                  fontsize=14, 
                  pad=15)
    ax1.set_ylabel('Total CO2 (kg)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Plot 2: Stacked bar chart of components
    components = ['car_km', 'bus_km', 'energy_kwh', 'meat_kg', 'veggie_kg']
    colors = ['#e74c3c', '#3498db', '#f1c40f', '#9b59b6', '#1abc9c']
    labels = ['Car (km)', 'Bus (km)', 'Energy (kWh)', 'Meat (kg)', 'Vegetables (kg)']
    
    df[components].plot(kind='bar', 
                       stacked=True, 
                       ax=ax2, 
                       color=colors)
    
    ax2.set_title('Breakdown of CO2 Sources', 
                  fontsize=14, 
                  pad=15)
    ax2.set_xlabel('Entry Number', fontsize=12)
    ax2.set_ylabel('Amount', fontsize=12)
    ax2.legend(labels, 
              title='Sources', 
              bbox_to_anchor=(1.05, 1), 
              loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate x-axis labels
    ax1.tick_params(axis='x', rotation=45)
    ax2.tick_params(axis='x', rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot to a bytes buffer with higher DPI for better quality
    buf = BytesIO()
    plt.savefig(buf, 
                format='png', 
                dpi=300, 
                bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return send_file(buf, mimetype='image/png')