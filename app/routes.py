from flask import Blueprint, request, jsonify, send_file
from .models import CO2Entry
from . import db
from .utils import calculate_co2, validate_data
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
import matplotlib.ticker as ticker
from base64 import b64encode
import json
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

    # Calculate new average after adding entry
    db.session.add(new_entry)
    db.session.commit()  # Commit here to ensure the new entry is included in the average
    
    all_entries = CO2Entry.query.with_entities(CO2Entry.total_co2).all()
    average_co2 = sum(entry[0] for entry in all_entries) / len(all_entries)
    
    # Update the result to include the average
    result["average_co2"] = round(average_co2, 1)

    # Generate base64 key from entry ID
    history_key = b64encode(str(new_entry.id).encode()).decode()
    
    # Add key to result
    result["history_key"] = history_key

    return jsonify(result)

@main.route("/visualization", methods=["GET"])
def get_visualization():
    entries = CO2Entry.query.all()
    
    if not entries:
        return "Keine Daten vorhanden", 404
        
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
    
    # Use a more modern style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Set a font that supports subscripts
    plt.rcParams['font.family'] = 'DejaVu Sans'
    # or try 'Liberation Sans' if DejaVu Sans is not available
    
    # Create figure with better spacing and higher resolution
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), dpi=100)
    
    # Plot 1: Enhanced Total CO2 over time
    ax1.plot(range(len(df['total_co2'])), df['total_co2'],
             marker='o',
             color='#2ecc71',
             linewidth=2,
             markersize=8,
             alpha=0.4,
             label='Individuelle Messungen')
    
    # Calculate total average
    total_average = df['total_co2'].mean()
    
    # Add average text annotation
    ax1.text(0.02, 0.95, 
             f'Gesamtdurchschnitt: {total_average:.1f} kg CO2',
             transform=ax1.transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3.0),
             fontsize=12,
             fontweight='bold')
    
    # Improved rolling average with longer window
    rolling_avg = df['total_co2'].rolling(window=5, min_periods=1).mean()
    ax1.plot(range(len(df['total_co2'])), rolling_avg,
             color='#27ae60',
             linewidth=3,
             label='Durchschnitt (5 Einträge)')
    
    ax1.fill_between(range(len(df['total_co2'])), rolling_avg,
                     alpha=0.2,
                     color='#27ae60')
    
    # Enhanced title and labels
    ax1.set_title('CO2 Ausstoß durchschnittlich',
                  fontsize=16,
                  fontweight='bold',
                  pad=20)
    ax1.set_ylabel('Totales CO2 (kg)', fontsize=14)
    ax1.set_xlabel('', fontsize=14)
    
    # Plot 2: Modifizierte Version für absolute CO2-Werte
    components = ['car_km', 'bus_km', 'energy_kwh', 'meat_kg', 'veggie_kg']
    co2_factors = {
        'car_km': 0.2,      # kg CO2 pro km
        'bus_km': 0.08,     # kg CO2 pro km
        'energy_kwh': 0.4,  # kg CO2 pro kWh
        'meat_kg': 13.3,    # kg CO2 pro kg
        'veggie_kg': 2.0    # kg CO2 pro kg
    }
    
    # Berechne absolute CO2-Werte für jede Quelle
    co2_data = pd.DataFrame()
    for comp in components:
        co2_data[comp] = df[comp] * co2_factors[comp]
    
    colors = ['#e74c3c', '#3498db', '#f1c40f', '#9b59b6', '#1abc9c']
    labels = ['Auto', 'Bus', 'Energie', 'Fleisch', 'Gemüse']
    
    co2_data.plot(kind='bar',
                 stacked=True,
                 ax=ax2,
                 color=colors)
    
    ax2.set_title('CO2 Ausstoß nach Quelle',
                  fontsize=16,
                  fontweight='bold',
                  pad=20)
    ax2.set_xlabel('', fontsize=14)
    ax2.set_ylabel('CO2 (kg)', fontsize=14)
    
    # Verbesserte Legende mit CO2-Werten
    total_co2_per_source = co2_data.sum()
    labels_with_total = [f'{label} ({total_co2_per_source.iloc[i]:.1f} kg)' 
                        for i, label in enumerate(labels)]
    
    ax2.legend(labels_with_total,
              title='CO2 Quellen (Gesamt)',
              bbox_to_anchor=(1.05, 1),
              loc='upper left',
              fontsize=12)
    
    # Improve tick labels and format y-axis to show integers
    for ax in [ax1, ax2]:
        ax.tick_params(axis='both', labelsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
        ax.set_xticklabels([])
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)
    
    # Add grid with better visibility
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # Add a subtle background color
    fig.patch.set_facecolor('#f8f9fa')
    
    # Adjust layout with more padding
    plt.tight_layout(pad=3.0)
    
    # Save with higher quality
    buf = BytesIO()
    plt.savefig(buf,
                format='png',
                dpi=300,
                bbox_inches='tight',
                facecolor=fig.get_facecolor(),
                edgecolor='none')
    buf.seek(0)
    plt.close()
    
    return send_file(buf, mimetype='image/png')

@main.route("/history/<key>", methods=["GET"])
def get_history(key):
    try:
        # Decode base64 key to get entry ID
        entry_id = int(b64encode(key.encode()).decode())
        entry = CO2Entry.query.get(entry_id)
        
        if not entry:
            return jsonify({"error": "Invalid key"}), 404
            
        return jsonify({
            "timestamp": entry.timestamp,
            "car_km": entry.car_km,
            "bus_km": entry.bus_km,
            "energy_kwh": entry.energy_kwh,
            "meat_kg": entry.meat_kg,
            "veggie_kg": entry.veggie_kg,
            "total_co2": entry.total_co2
        })
    except:
        return jsonify({"error": "Invalid key"}), 400