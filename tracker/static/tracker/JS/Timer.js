document.addEventListener('DOMContentLoaded', () => {
    let timerInterval;

    let isRunning = localStorage.getItem('isRunning') === 'true';
    let startTime = parseInt(localStorage.getItem('startTime')) || 0;
    let elapsedTime = parseInt(localStorage.getItem('elapsedTime')) || 0;

    const display = document.getElementById('display');
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const stopBtn = document.getElementById('stop-btn');
    const logBtn = document.getElementById('log-btn');

    function updateDisplay(time) {
        let diffInHrs = time / 3600000;
        let hh = Math.floor(diffInHrs);

        let diffInMin = (diffInHrs - hh) * 60;
        let mm = Math.floor(diffInMin);

        let diffInSec = (diffInMin - mm) * 60;
        let ss = Math.floor(diffInSec);

        let formattedHH = hh.toString().padStart(2, "0");
        let formattedMM = mm.toString().padStart(2, "0");
        let formattedSS = ss.toString().padStart(2, "0");

        display.innerHTML = `${formattedHH}:${formattedMM}:${formattedSS}`;
    }

    if (isRunning) {
        startTimer();
    } else {
        updateDisplay(elapsedTime); 
    }

    function startTimer() {
        clearInterval(timerInterval);
        
        if (!isRunning) {
            startTime = Date.now() - elapsedTime;
            localStorage.setItem('startTime', startTime);
            localStorage.setItem('isRunning', 'true');
            isRunning = true;
        }

        timerInterval = setInterval(() => {
            elapsedTime = Date.now() - startTime;
            updateDisplay(elapsedTime);
        }, 1000); 
    }

    function pauseTimer() {
        clearInterval(timerInterval);
        
        isRunning = false;
        localStorage.setItem('isRunning', 'false');
        localStorage.setItem('elapsedTime', elapsedTime);
    }

    function stopTimer() {
        clearInterval(timerInterval);
        
        elapsedTime = 0;
        isRunning = false;
        
        
        localStorage.removeItem('isRunning');
        localStorage.removeItem('startTime');
        localStorage.removeItem('elapsedTime');
        
        updateDisplay(elapsedTime);
    }

    async function logHours() {
        pauseTimer(); 
        
        
        let totalSeconds = Math.floor(elapsedTime / 1000);
        let hoursLogged = (totalSeconds / 3600).toFixed(2); 

        
        if (hoursLogged <= 0) {
            alert("Timer hasn't started yet!");
            return;
        }

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        
        const formData = new FormData();
        formData.append('hours', hoursLogged);

        try {
            const response = await fetch('/dashboard/', { 
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                alert(`Success! Logged ${hoursLogged} hours.`);
                stopTimer(); 
            } else {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            console.error('Error logging time:', error);
            alert("Something went wrong trying to connect to the server.");
        }
    }

    
    startBtn.addEventListener('click', startTimer);
    pauseBtn.addEventListener('click', pauseTimer);
    stopBtn.addEventListener('click', stopTimer);
    logBtn.addEventListener('click', logHours);
});