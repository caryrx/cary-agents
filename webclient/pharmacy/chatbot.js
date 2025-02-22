window.onload = function () {
    window.WebChat.default(
        {
            initPayload: "/greet",
            customData: { "bot_name": "rejoyn" },
            socketUrl: "http://localhost:5010", // Bot API
            socketPath: "/socket.io/",
            title: "Rejoyn Bot",
            subtitle: "Ask me about Rejoyn",
            inputTextFieldHint: "Type your message...",
            showFullScreenButton: true,
            showMessageDate: true,
            params: {
                storage: "session"
            }
        },
        null
    );
};

