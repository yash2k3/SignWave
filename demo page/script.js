// Function to generate text based on selected language
function generateText() {
    let predictedText = "Hello, how are you?"; // Simulated model prediction
    let selectedLanguage = document.getElementById("languageDropdown").value.toLowerCase(); // Convert to lowercase for comparison

    let finalOutputText;
    switch (selectedLanguage) {
        case 'telugu':
            finalOutputText = "హలో ఎలా ఉన్నారు"; // Example translation
            break;
        case 'hindi':
            finalOutputText = "नमस्ते, आप कैसे हैं"; // Example translation
            break;
        default:
            finalOutputText = predictedText;
    }

    // Update the final output text
    document.getElementById("finalOutput").innerText = finalOutputText;

    // Clear the predicted text area
    document.getElementById("predictedText").innerText = "";

    // Initialize typed.js for animated typing effect without looping or backspacing
    new Typed(".auto-type", {
        strings: [predictedText],
        typeSpeed: 160,
        backSpeed: 0, // No reverse motion
        loop: false
    });
}

// Get the video element
const videoPlayer = document.getElementById("videoPlayer");

// Add an event listener to the video for when it starts playing
videoPlayer.addEventListener("play", function() {
    // Trigger the generateText function when the video starts playing
    generateText();
});
