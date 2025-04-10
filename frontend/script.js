let recognition;
let isListening = false;
let isProcessing = false;
let isSpeaking = false; // New flag for speaking state
let timeout;
const backendURL = "http://127.0.0.1:8000/transcribe"; // Backend URL

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    const languageOptions = {
        'English (US)': 'en-US',
        'English (UK)': 'en-GB',
        'German (Germany)': 'de-DE'
    };

    const languageSelect = document.getElementById('language-select');
    for (const [label, lang] of Object.entries(languageOptions)) {
        const option = document.createElement('option');
        option.value = lang;
        option.textContent = label;
        languageSelect.appendChild(option);
    }

    languageSelect.addEventListener('change', () => {
        recognition.lang = languageSelect.value;
    });

    recognition.onresult = (event) => {
        let transcript = event.results[event.results.length - 1][0].transcript.trim();

        if (transcript) {
            addChatMessage("User", transcript);
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                sendToBackend(transcript);
            }, 1000);
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech Recognition Error:', event.error);
    };
}

document.getElementById('start-conversation').addEventListener('click', () => {
    document.getElementById('mic-btn').disabled = false;
    startListening();
});

document.getElementById('mic-btn').addEventListener('click', () => {
    if (!isProcessing && !isSpeaking) {
        if (!isListening) {
            startListening();
        } else {
            stopListening();
        }
    }
});

function startListening() {
    if (recognition && !isSpeaking) {
        recognition.start();
        document.getElementById('mic-btn').classList.add('listening');
        document.getElementById('mic-btn').classList.remove('sending');
        isListening = true;
    }
}

function stopListening() {
    if (recognition) {
        recognition.stop();
        document.getElementById('mic-btn').classList.remove('listening');
        isListening = false;
    }
}

function sendToBackend(transcript) {
    if (!transcript.trim()) return;

    stopListening();
    isProcessing = true;
    document.getElementById('mic-btn').classList.add('sending');

    fetch(backendURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ transcription: transcript })
    })
        .then(response => response.json())
        .then(data => {
            addChatMessage("AI", data.response);
            speakText(data.response); // Convert text to speech
        })
        .catch(error => console.error("Error sending data:", error));
}

// 🔹 Web Speech API TTS Function
function speakText(text) {
    if ('speechSynthesis' in window) {
        let speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'en-US'; // Adjust language
        isSpeaking = true; // Set flag to prevent listening during speech
        stopListening(); // Stop mic when speaking
        document.getElementById('mic-btn').classList.add('sending'); // Indicate speaking state

        speech.onend = function () {
            isSpeaking = false;
            document.getElementById('mic-btn').classList.remove('sending');
            startListening(); // Resume listening after speech is done
        };

        window.speechSynthesis.speak(speech);
    } else {
        console.error("Text-to-Speech not supported in this browser.");
    }
}

function addChatMessage(speaker, message) {
    let chatBox = document.getElementById('chat-box');
    let messageElement = document.createElement('div');
    messageElement.classList.add("message", speaker === "User" ? "user-message" : "ai-message");
    messageElement.innerHTML = `<strong>${speaker}:</strong> ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
