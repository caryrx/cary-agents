#!/bin/bash

# Check if bot name is provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/start_bot.sh <bot_name> [port]"
    exit 1
fi

BOT_NAME=$1
PORT=${2:-5010}  # Default to port 5010 if not provided

LOG_DIR="logs"
if [ ! -d "$LOG_DIR" ]; then
	echo "Creating logs directory..."
	mkdir -p "$LOG_DIR"
fi


# Start the selected bot
echo "Starting $BOT_NAME bot on port $PORT..."
rasa run --model models/$BOT_NAME --endpoints endpoints.yml --credentials credentials.yml --enable-api --cors ["*","http://localhost:6010"] --port $PORT > logs/$BOT_NAME.log 2>&1 &

echo "$BOT_NAME bot started on http://localhost:$PORT"

# Start a simple web server for the web client (optional)
WEB_PORT=$((PORT + 1000))  # Web client runs on a different port
WEB_DIR="webclient/$BOT_NAME"

if [ -d "$WEB_DIR" ]; then
    echo "Starting web client for $BOT_NAME on port $WEB_PORT..."
    cd $WEB_DIR

    if [ ! -d "../$LOG_DIR" ]; then
        echo "Creating logs directory for web client..."
        mkdir -p "../$LOG_DIR"
    fi


    python3 -m http.server $WEB_PORT > ../logs/$BOT_NAME-web.log 2>&1 &
    echo "Web client available at http://localhost:$WEB_PORT"
    cd - > /dev/null
else
    echo "No web client found for $BOT_NAME. Skipping..."
fi

