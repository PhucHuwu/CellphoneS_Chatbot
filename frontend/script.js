document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const sendButton = document.getElementById("send-button");
    const typingIndicator = document.getElementById("typing-indicator");
    const quickActions = document.getElementById("quick-actions");

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString("vi-VN", {
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    function formatMarkdown(text) {
        // Convert markdown to HTML
        let html = text
            // Headers
            .replace(/^### (.*$)/gim, "<h3>$1</h3>")
            .replace(/^## (.*$)/gim, "<h2>$1</h2>")
            .replace(/^# (.*$)/gim, "<h1>$1</h1>")

            // Bold text
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(/__(.*?)__/g, "<strong>$1</strong>")

            // Italic text
            .replace(/\*(.*?)\*/g, "<em>$1</em>")
            .replace(/_(.*?)_/g, "<em>1</em>")

            // Code blocks
            .replace(/\`\`\`([\s\S]*?)\`\`\`/g, "<pre><code>$1</code></pre>")
            .replace(/`(.*?)`/g, "<code>$1</code>")

            // Markdown links [text](url)
            .replace(
                /\[([^\]]+)\]$$([^)]+)$$/g,
                '<a href="$2" target="_blank" rel="noopener noreferrer" class="chat-link">$1 <i class="fas fa-external-link-alt"></i></a>'
            )

            // Auto-detect URLs (http, https, www)
            .replace(
                /(https?:\/\/[^\s<>"{}|\\^`[\]]+)/g,
                '<a href="$1" target="_blank" rel="noopener noreferrer" class="chat-link auto-link">$1 <i class="fas fa-external-link-alt"></i></a>'
            )
            .replace(
                /(?<!https?:\/\/)(www\.[^\s<>"{}|\\^`[\]]+)/g,
                '<a href="https://$1" target="_blank" rel="noopener noreferrer" class="chat-link auto-link">$1 <i class="fas fa-external-link-alt"></i></a>'
            )

            // Phone numbers (Vietnamese format)
            .replace(
                /(\+84|0)([0-9]{9,10})/g,
                '<a href="tel:$1$2" class="chat-link phone-link"><i class="fas fa-phone"></i> $1$2</a>'
            )

            // Email addresses
            .replace(
                /([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g,
                '<a href="mailto:$1" class="chat-link email-link"><i class="fas fa-envelope"></i> $1</a>'
            )

            // Line breaks
            .replace(/\n\n/g, "</p><p>")
            .replace(/\n/g, "<br>")

            // Lists
            .replace(/^\d+\.\s+(.*$)/gim, "<li>$1</li>")
            .replace(/^[\-\*\+]\s+(.*$)/gim, "<li>$1</li>")

            // Wrap in paragraphs
            .replace(/^(?!<[h|l|p|d])/gm, "<p>")
            .replace(/(?<!>)$/gm, "</p>")

            // Clean up extra paragraph tags
            .replace(/<p><\/p>/g, "")
            .replace(/<p>(<[h|l])/g, "$1")
            .replace(/(<\/[h|l][^>]*>)<\/p>/g, "$1")

            // Wrap list items in ul/ol
            .replace(/(<li>.*<\/li>)/gs, function (match) {
                // Check if it's a numbered list
                const isNumbered = /^\d+\./.test(
                    text.match(/^\d+\.\s+.*$/m)?.[0] || ""
                );
                const tag = isNumbered ? "ol" : "ul";
                return `<${tag}>${match}</${tag}>`;
            });

        // Clean up and format the HTML
        html = html
            .replace(/<p><br>/g, "<p>")
            .replace(/<br><\/p>/g, "</p>")
            .replace(/(<\/[uo]l>)<\/p>/g, "$1")
            .replace(/<p>(<[uo]l>)/g, "$1");

        return html;
    }

    function handleLinkClicks(messageElement) {
        const links = messageElement.querySelectorAll(".chat-link");
        links.forEach((link) => {
            link.addEventListener("click", function (e) {
                // Add click animation
                this.style.transform = "scale(0.95)";
                setTimeout(() => {
                    this.style.transform = "scale(1)";
                }, 150);

                // Track link clicks (optional analytics)
                console.log("Link clicked:", this.href);

                // For phone links, show confirmation on mobile
                if (
                    this.classList.contains("phone-link") &&
                    /Mobi|Android/i.test(navigator.userAgent)
                ) {
                    if (
                        !confirm("Bạn có muốn gọi điện thoại đến số này không?")
                    ) {
                        e.preventDefault();
                    }
                }
            });
        });
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message");

        const isUser = sender === "user";
        const messageClass = isUser ? "user-message" : "bot-message";
        const bubbleClass = isUser ? "user-bubble" : "bot-bubble";
        const avatarIcon = isUser ? "fas fa-user" : "fas fa-robot";

        // Format text if it's from bot
        const formattedText = isUser ? text : formatMarkdown(text);

        msgDiv.innerHTML = `
            <div class="${messageClass}">
                <div class="message-avatar">
                    <i class="${avatarIcon}"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble ${bubbleClass}">
                        ${formattedText}
                    </div>
                    <div class="message-time">${getCurrentTime()}</div>
                </div>
            </div>
        `;

        chatBox.appendChild(msgDiv);

        // Handle link clicks for bot messages
        if (!isUser) {
            handleLinkClicks(msgDiv);
        }

        chatBox.scrollTop = chatBox.scrollHeight;

        // Hide quick actions after first message
        if (sender === "user") {
            quickActions.style.display = "none";
        }
    }

    function showTypingIndicator() {
        typingIndicator.style.display = "flex";
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = "none";
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            sendButton.disabled = true;
            sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            chatForm.classList.add("loading");
        } else {
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
            chatForm.classList.remove("loading");
        }
    }

    function sendMessage(message) {
        if (!message.trim()) return;

        // Add user message
        appendMessage("user", message);
        userInput.value = "";

        // Show loading state
        setLoadingState(true);
        showTypingIndicator();

        // Simulate network delay for better UX
        setTimeout(() => {
            fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: message }),
            })
                .then((res) => res.json())
                .then((data) => {
                    hideTypingIndicator();
                    setLoadingState(false);

                    if (data.answer) {
                        appendMessage("bot", data.answer);
                    } else {
                        appendMessage(
                            "bot",
                            "Xin lỗi, tôi không thể trả lời câu hỏi này lúc này. Vui lòng thử lại sau hoặc liên hệ với bộ phận hỗ trợ khách hàng."
                        );
                    }
                })
                .catch(() => {
                    hideTypingIndicator();
                    setLoadingState(false);
                    appendMessage(
                        "bot",
                        "Không thể kết nối tới máy chủ. Vui lòng kiểm tra kết nối internet và thử lại."
                    );
                });
        }, 800); // Small delay to show typing indicator
    }

    // Form submission
    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const query = userInput.value.trim();
        sendMessage(query);
    });

    // Quick actions
    quickActions.addEventListener("click", function (e) {
        const quickActionItem = e.target.closest(".quick-action-item");
        if (quickActionItem) {
            const message = quickActionItem.getAttribute("data-message");
            sendMessage(message);
        }
    });

    // Header actions
    document
        .querySelector(".header-actions")
        .addEventListener("click", function (e) {
            const btn = e.target.closest(".action-btn");
            if (btn) {
                const icon = btn.querySelector("i");
                if (icon.classList.contains("fa-refresh")) {
                    // Refresh chat
                    location.reload();
                } else if (icon.classList.contains("fa-cog")) {
                    // Settings (placeholder)
                    appendMessage(
                        "bot",
                        "Tính năng cài đặt sẽ được cập nhật trong phiên bản tiếp theo."
                    );
                }
            }
        });

    // Auto-focus input when page loads
    userInput.focus();

    // Handle Enter key press
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event("submit"));
        }
    });

    // Auto-resize input
    userInput.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = Math.min(this.scrollHeight, 120) + "px";
    });

    // Attachment and emoji buttons (placeholder functionality)
    document
        .querySelector(".attachment-btn")
        .addEventListener("click", function () {
            appendMessage(
                "bot",
                "Tính năng đính kèm file sẽ được cập nhật trong phiên bản tiếp theo."
            );
        });

    document.querySelector(".emoji-btn").addEventListener("click", function () {
        appendMessage(
            "bot",
            "Tính năng emoji sẽ được cập nhật trong phiên bản tiếp theo."
        );
    });

    // Smooth scroll animation
    function smoothScrollToBottom() {
        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: "smooth",
        });
    }

    // Update scroll function
    const originalAppendMessage = appendMessage;
    appendMessage = function (sender, text) {
        originalAppendMessage(sender, text);
        setTimeout(smoothScrollToBottom, 100);
    };
});
