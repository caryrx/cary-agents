#!/bin/bash

# Check if bot name is provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/stop_bot.sh <bot_name>"
    exit 1
fi

BOT_NAME=$1

# Find and kill the Rasa bot process
echo "Stopping $BOT_NAME bot..."
BOT_PID=$(ps aux | grep "rasa run --model models/$BOT_NAME" | grep -v grep | awk '{print $2}')

if [ -n "$BOT_PID" ]; then
    kill $BOT_PID
    echo "$BOT_NAME bot stopped."
else
    echo "No running process found for $BOT_NAME bot."
fi

# Find and kill the web client process (assumed to be running via Python server)
WEB_PID=$(ps -ef | grep "http.server" | grep Python | grep -v grep | awk '{print $2}')

if [ -n "$WEB_PID" ]; then
    kill $WEB_PID
    echo "Web client for $BOT_NAME stopped."
else
    echo "No running web client found for $BOT_NAME."
fi

