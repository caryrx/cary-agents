#!/bin/bash

BOT_NAME=$1

if [[ -z "$BOT_NAME" ]]; then
    echo "Usage: ./scripts/train_agent.sh <bot_name>"
    exit 1
fi

rasa train --data bots/$BOT_NAME --domain bots/$BOT_NAME/domain.yml --config config/config_$BOT_NAME.yml --out models/$BOT_NAME

