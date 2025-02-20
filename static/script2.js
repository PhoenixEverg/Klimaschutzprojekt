// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Array of songs
    const playlist = [
        "static/music/Live and Learn.mp3",
        "static/music/Youre Just Like Pop Music.mp3"
    ];
    
    let currentSong = 0;
    const audioPlayer = document.getElementById("audioPlayer");

    // Set initial song
    audioPlayer.src = playlist[currentSong];
    audioPlayer.loop = false;  // Remove individual song looping
    audioPlayer.play().catch(e => console.log("Autoplay prevented:", e));

    // When one song ends, play the next one
    audioPlayer.addEventListener('ended', function() {
        currentSong = (currentSong + 1) % playlist.length; // Loop back to start if at end
        audioPlayer.src = playlist[currentSong];
        audioPlayer.play().catch(e => console.log("Playback error:", e));
    });

    // Add page transition handler
    document.querySelector('.nav-button').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default navigation
        
        // Stop the audio
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        
        // Add fade-out animation to all main elements
        document.querySelector('.intro').classList.add('fade-out');
        document.querySelector('.nav-button').classList.add('fade-out');
        document.querySelector('.music-button').classList.add('fade-out');
        
        // Wait for animation to complete before changing page
        setTimeout(() => {
            window.location.href = 'Calculator.html';
        }, 1000); // Match this with animation duration
    });

    const musicButton = document.querySelector('.music-button');
    let isPlaying = false;

    musicButton.addEventListener('click', function(e) {
        e.preventDefault();
        if (isPlaying) {
            audioPlayer.pause();
            musicButton.textContent = "▶ © 2025-2025 Oliver, Malik, Mika";
        } else {
            audioPlayer.play().catch(e => console.log("Playback error:", e));
            musicButton.textContent = "⏸ © 2025-2025 Oliver, Malik, Mika";
        }
        isPlaying = !isPlaying;
    });

    // Login system
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const closeBtn = document.querySelector('.close');

    loginBtn.onclick = function() {
        loginModal.style.display = "block";
    }

    closeBtn.onclick = function() {
        loginModal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == loginModal) {
            loginModal.style.display = "none";
        }
    }
});

// Move validateKey outside the DOMContentLoaded listener
function validateKey() {
    const keyInput = document.getElementById('keyInput').value;
    try {
        const decodedKey = atob(keyInput);
        const [co2Value, timestamp] = decodedKey.split('-');
        
        if (co2Value && timestamp) {
            window.location.href = `result.html?co2=${co2Value}&key=${keyInput}`;
        } else {
            alert('Ungültiger CO₂-Key');
        }
    } catch (error) {
        alert('Ungültiger CO₂-Key');
    }
}