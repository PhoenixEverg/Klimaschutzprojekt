async function calculateCO2() {
    const data = {
        car: parseFloat(document.getElementById('car').value) || 0,
        bus: parseFloat(document.getElementById('bus').value) || 0,
        bike: parseFloat(document.getElementById('bike').value) || 0,
        meat: parseFloat(document.getElementById('meat').value) || 0,
        veggie: parseFloat(document.getElementById('veggie').value) || 0,
        energy: parseFloat(document.getElementById('energy').value) || 0
    };

    try {
        const response = await fetch('https://concise-partly-colt.ngrok-free.app/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'ngrok-skip-browser-warning': 'true'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        const resultDiv = document.getElementById('result');
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <p>Gesamt CO₂-Ausstoß: ${result.total_co2.toFixed(2)} kg</p>
            <h3>Verbesserungsvorschläge:</h3>
            <ul>
                ${result.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
            </ul>
        `;
    } catch (error) {
        console.error('Error:', error);
        alert('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.');
    }
}
