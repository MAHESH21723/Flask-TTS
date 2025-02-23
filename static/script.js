document.addEventListener("DOMContentLoaded", function () {
    const textInput = document.getElementById("textInput");
    const speakButton = document.getElementById("speakBtn");
    const downloadButton = document.getElementById("downloadBtn");
    const audioPlayer = document.getElementById("audioPlayer");
    const speechEffect = document.getElementById("speechEffect");

    speakButton.addEventListener("click", async function () {
        const text = textInput.value.trim();
        if (!text) {
            alert("Please enter text before speaking!");
            return;
        }

        try {
            const response = await fetch("/generate_audio", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text, lang: "en" })
            });

            const data = await response.json();
            if (data.audio_url) {
                audioPlayer.src = data.audio_url;
                audioPlayer.play();

                // Show speech effect while audio is playing
                speechEffect.style.display = "flex";

                audioPlayer.onended = function () {
                    speechEffect.style.display = "none"; // Hide when finished
                };
            } else {
                alert("Error: " + data.error);
            }
        } catch (error) {
            alert("Request failed: " + error);
        }
    });

    downloadButton.addEventListener("click", function () {
        window.location.href = "/download_audio";
    });
});
