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
        const co2Value = result.total_co2.toFixed(2);
        
        // Weiterleitung mit URL-Parameter
        window.location.href = `result.html?co2=${co2Value}`;

    } catch (error) {
        console.error('Fehler:', error);
        alert('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.');
    }
}

// Funktion zum Anzeigen des Ergebnisses auf der result.html Seite
function showResult() {
    const resultDiv = document.getElementById('result');
    if (resultDiv) {
        const co2Result = localStorage.getItem('co2Result');
        if (co2Result) {
            resultDiv.innerHTML = `
                <h2>Dein CO₂-Ausstoß ist: ${co2Result} kg</h2>
            `;
            resultDiv.style.display = 'block';
            setTimeout(() => {
                resultDiv.classList.add('active');
            }, 50);
            // Löschen Sie das Ergebnis aus dem localStorage
            localStorage.removeItem('co2Result');
        }
    }
}

// Führen Sie showResult aus, wenn die Seite geladen wird
document.addEventListener('DOMContentLoaded', showResult);
