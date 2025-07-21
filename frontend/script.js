document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message");
        msgDiv.innerHTML = `<span class="${sender}">${
            sender === "user" ? "Bạn" : "Bot"
        }:</span> ${text}`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;
        appendMessage("user", query);
        userInput.value = "";
        fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.answer) {
                    appendMessage("bot", data.answer);
                } else {
                    appendMessage(
                        "bot",
                        "Đã xảy ra lỗi hoặc không có câu trả lời."
                    );
                }
            })
            .catch(() => {
                appendMessage("bot", "Không thể kết nối tới máy chủ.");
            });
    });
});
