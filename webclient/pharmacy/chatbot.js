window.onload = function () {
    window.WebChat.default(
        {
            initPayload: "/greet",
            customData: { "bot_name": "pharmacy" },
            socketUrl: "http://localhost:5010", // Bot API
            socketPath: "/socket.io/",
            title: "Pharmacy Bot",
            subtitle: "Ask me about Pharmacy",
            inputTextFieldHint: "Type your message...",
            showFullScreenButton: true,
            showMessageDate: true,
            params: {
                storage: "none"
            }
        },
        null
    );
};

