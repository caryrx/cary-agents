# Rasa Multi-Agent Bot Framework

This repository contains multiple Rasa chatbots that can be trained, deployed, and managed independently within a single project. Each bot has its own intents, domain, and training data.

---

## 📌 Project Overview

This project allows you to:
- Train multiple Rasa bots independently.
- Start and stop bots dynamically.
- Serve bots via REST API or WebSockets.
- Integrate Rasa WebChat for a web-based chat UI.
- Store and manage models efficiently.

---

## 📂 Getting Started

1. Create a venv with python 3.10 environment with python3.10 -m venv venv
2. pip install -r requirements.txt
3. train your model with sh ./train_agent.sh pharmacy
4. run the action server with rasa run actions [--debug]
5. start an agent with ./start_agent.sh pharmacy
6. go to http://localhost:6010/
7. ask 'can you deliver to zipcode 20001'
8. ask it if the pharmacy is busy today 


