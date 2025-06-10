document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keydown", function(e) {
    if (e.key === "Enter") sendMessage();
});

function appendMessage(content, className) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.className = `chat-bubble ${className}`;
    messageDiv.textContent = content;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value.trim();
    if (message === "") return;

    appendMessage(message, "user-bubble");
    userInput.value = "";

    // Show loading spinner
    document.getElementById("loading-spinner").classList.remove("hidden");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        if (data.reply) {
            appendMessage(data.reply, "bot-bubble");
        } else {
            appendMessage("Sorry, there was an error.", "bot-bubble");
        }
    } catch (error) {
        appendMessage("Sorry, there was an error.", "bot-bubble");
        console.error("Error:", error);
    }

    // Hide loading spinner
    document.getElementById("loading-spinner").classList.add("hidden");
}
