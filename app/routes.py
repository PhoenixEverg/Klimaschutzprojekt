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

    # Calculate new average after adding entry
    db.session.add(new_entry)
    db.session.commit()  # Commit here to ensure the new entry is included in the average
    
    all_entries = CO2Entry.query.with_entities(CO2Entry.total_co2).all()
    average_co2 = sum(entry[0] for entry in all_entries) / len(all_entries)
    
    # Update the result to include the average
    result["average_co2"] = round(average_co2, 1)

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
    
    # Create figure with better spacing and higher resolution
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), dpi=100)
    
    # Plot 1: Enhanced Total CO2 over time
    ax1.plot(range(len(df['total_co2'])), df['total_co2'],
             marker='o',
             color='#2ecc71',
             linewidth=2,
             markersize=8,
             alpha=0.4,
             label='Individual measurements')
    
    # Calculate total average
    total_average = df['total_co2'].mean()
    
    # Add average text annotation
    ax1.text(0.02, 0.95, 
             f'Gesamtdurchschnitt: {total_average:.1f} kg CO₂',
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
    ax1.set_xlabel('Eintrag', fontsize=14)
    
    # Plot 2: Enhanced stacked bar chart
    components = ['car_km', 'bus_km', 'energy_kwh', 'meat_kg', 'veggie_kg']
    colors = ['#e74c3c', '#3498db', '#f1c40f', '#9b59b6', '#1abc9c']
    labels = ['Auto', 'Bus', 'Energie', 'Fleisch', 'Gemüse']
    
    # Calculate percentage for each component
    df_percent = df[components].div(df[components].sum(axis=1), axis=0) * 100
    
    df_percent.plot(kind='bar',
                   stacked=True,
                   ax=ax2,
                   color=colors)
    
    ax2.set_title('CO2 Quellenverteilung',
                  fontsize=16,
                  fontweight='bold',
                  pad=20)
    ax2.set_xlabel('Eintrag', fontsize=14)
    ax2.set_ylabel('Prozent (%)', fontsize=14)
    
    # Enhanced legend
    ax2.legend(labels,
              title='CO2 Quellen',
              bbox_to_anchor=(1.05, 1),
              loc='upper left',
              fontsize=12)
    
    # Improve tick labels
    for ax in [ax1, ax2]:
        ax.tick_params(axis='both', labelsize=12)
        ax.tick_params(axis='x', rotation=45)
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