import os
import requests
from gpt4all import GPT4All
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
from typing import Text, Dict, Any, List


# Paths to local GPT4All model
GPT4ALL_MODEL_PATH = "/Users/matt/Library/Application Support/nomic.ai/GPT4All/Llama-3.2-3B-Instruct-Q4_0.gguf"

# Mock API URLs (Replace with real endpoints)
ORDER_API_URL = "https://api.example.com/order_status"
STOCK_API_URL = "https://api.example.com/check_stock"

# Load GPT4All model
gpt_model = GPT4All(model_name=GPT4ALL_MODEL_PATH)

class ActionCheckOrderStatus(Action):
    def name(self):
        return "action_check_order_status"

    def run(self, dispatcher, tracker, domain):
        order_id = next(tracker.get_latest_entity_values("order_id"), None)
        if not order_id:
            dispatcher.utter_message(text="I need an order ID to check the status.")
            return []
        
        response = requests.get(f"{ORDER_API_URL}?order_id={order_id}")
        if response.status_code == 200:
            order_status = response.json().get("status", "unknown")
            dispatcher.utter_message(text=f"Your order status: {order_status}")
        else:
            dispatcher.utter_message(text="I couldn't fetch order status. Please try again later.")
        
        return []

class ActionCheckStock(Action):
    def name(self):
        return "action_check_stock"

    def run(self, dispatcher, tracker, domain):
        product = next(tracker.get_latest_entity_values("product"), None)
        if not product:
            dispatcher.utter_message(text="Which product are you checking stock for?")
            return []
        
        response = requests.get(f"{STOCK_API_URL}?product={product}")
        if response.status_code == 200:
            stock_info = response.json().get("availability", "unknown")
            dispatcher.utter_message(text=f"Stock status for {product}: {stock_info}")
        else:
            dispatcher.utter_message(text="I couldn't check stock. Please try again later.")
        
        return []

class ActionFallbackGPT4All(Action):
    def name(self):
        return "action_fallback_gpt4all"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()

        # Define responses for common small talk
        small_talk_responses = {
            "how are you": "I am doing well! Thanks for asking.",
            "who are you": "I am Kevin, your friendly pharmacy technician!",
            "what's your name": "I'm Kevin, the pharmacy technician. How can I help you today?"
        }

        for phrase, response in small_talk_responses.items():
            if phrase in user_message:
                dispatcher.utter_message(text=response)
                return []

        # Generate response using GPT4All
        with gpt_model.chat_session():
            bot_response = gpt_model.generate(prompt=f"You are Kevin, a pharmacy technician for CaryRx. Answer only pharmacy-related questions without giving drug advice. If the question is outside pharmacy, make up a plausible answer. {user_message}", temp=0.7)

        dispatcher.utter_message(text=bot_response)
        return []

class ActionCheckStock(Action):
    def name(self) -> Text:
        return "action_check_stock"

    def run(self, dispatcher, tracker, domain):
        drug = next(tracker.get_latest_entity_values("drug"), None)
        if not drug:
            dispatcher.utter_message(text="Which medication are you checking?")
            return []
        
        dispatcher.utter_message(text=f"Let me check stock for {drug}...")
        # Add API call or database lookup here

        return []


class ActionCheckDelivery(Action):
    def name(self) -> Text:
        return "action_check_delivery"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        zipcode = next(tracker.get_latest_entity_values("zipcode"), None)

        if not zipcode:
            dispatcher.utter_message(text="Which ZIP code are you checking?")
            return []

        dispatcher.utter_message(text=f"Checking delivery availability for ZIP code {zipcode}...")

        # API Request
        api_url = f"https://api5.caryrx.com/v1/zipcodes/{zipcode}"
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Assuming API response contains a key like "delivers" (True/False)
            dispatcher.utter_message(text=f"{data}!")

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="I couldn't check delivery at the moment. Please try again later.")

        return []
