def calculate_co2(data):
    # Realistischere CO₂-Faktoren
    transport = data.get("transport", 0) * 0.14  # ~140g CO₂ pro km (Durchschnittswert für PKW)
    energy = data.get("energy", 0) * 0.366      # ~366g CO₂ pro kWh (deutscher Strommix 2023)
    food = data.get("food", 0)                  # Direkte Eingabe der CO₂-Werte für Ernährung

    total = transport + energy + food

    # Vorschläge basierend auf den Daten
    suggestions = []
    if transport > 50:
        suggestions.append("Nutze öfter öffentliche Verkehrsmittel oder das Fahrrad.")
    if energy > 100:
        suggestions.append("Wechsle zu Ökostrom und senke deinen Energieverbrauch.")
    if food > 50:
        suggestions.append("Reduziere deinen Fleischkonsum und iss regional.")

    return {"total_co2": total, "suggestions": suggestions}