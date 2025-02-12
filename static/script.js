function nextSection(sectionNumber) {
    // Remove active class from all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
        section.classList.add('slide-right');
        section.classList.remove('slide-left');
    });
    
    // Hide all sections and remove transform classes
    setTimeout(() => {
        document.querySelectorAll('.section').forEach(section => {
            section.style.display = 'none';
            section.classList.remove('slide-right');
            section.classList.remove('slide-left');
        });
        
        // Show and animate new section
        const newSection = document.getElementById(`section${sectionNumber}`);
        newSection.style.display = 'block';
        newSection.classList.add('slide-left');
        setTimeout(() => {
            newSection.classList.remove('slide-left');
            newSection.classList.add('active');
        }, 50);
    }, 500);

    // Update progress bar
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });
    document.querySelector(`[data-step="${sectionNumber}"]`).classList.add('active');
}

function previousSection(sectionNumber) {
    // Remove active class and add slide-left animation
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
        section.classList.add('slide-left');
        section.classList.remove('slide-right');
    });
    
    setTimeout(() => {
        document.querySelectorAll('.section').forEach(section => {
            section.style.display = 'none';
            section.classList.remove('slide-right');
            section.classList.remove('slide-left');
        });
        
        const newSection = document.getElementById(`section${sectionNumber}`);
        newSection.style.display = 'block';
        newSection.classList.add('slide-right');
        setTimeout(() => {
            newSection.classList.remove('slide-right');
            newSection.classList.add('active');
        }, 50);
    }, 500);

    // Update progress bar
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });
    document.querySelector(`[data-step="${sectionNumber}"]`).classList.add('active');
}

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
        
        // Add animation to result
        setTimeout(() => {
            resultDiv.classList.add('active');
        }, 50);

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
