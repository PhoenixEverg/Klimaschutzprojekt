async function calculateCO2() {
    const transport = document.getElementById('transport').value;
    const food = document.getElementById('food').value;
    const energy = document.getElementById('energy').value;

    const data = {
        transport: parseFloat(transport),
        food: parseFloat(food),
        energy: parseFloat(energy)
    };

    try {
        const response = await fetch('http://localhost:5000/calculate', {
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

        if (result.total_co2 > 1000) {
            document.body.classList.add('dark-background');
        } else {
            document.body.classList.remove('dark-background');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.');
    }
}