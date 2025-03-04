import os
import requests
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Dict, Any, List

# Environment Variables
OLLAMA_HOST = "http://172.31.87.0:11434/"
ORDER_API_URL = "https://api.example.com/order_status"
STOCK_API_URL = "https://api.example.com/check_stock"
DELIVERY_API_URL = "https://api5.caryrx.com/v1/zipcodes/"

class ActionCheckOrderStatus(Action):
    def name(self):
        return "action_check_order_status"

    def run(self, dispatcher, tracker, domain):
        order_id = next(tracker.get_latest_entity_values("order_id"), None)
        if not order_id:
            dispatcher.utter_message(text="I need an order ID to check the status.")
            return []
        
        try:
            response = requests.get(f"{ORDER_API_URL}?order_id={order_id}", timeout=5)
            response.raise_for_status()
            order_status = response.json().get("status", "unknown")
            dispatcher.utter_message(text=f"Your order status: {order_status}")
        except requests.exceptions.RequestException:
            dispatcher.utter_message(text="I couldn't fetch order status. Please try again later.")
        
        return []

class ActionCheckStock(Action):
    def name(self) -> Text:
        return "action_check_stock"

    def run(self, dispatcher, tracker, domain):
        product = next(tracker.get_latest_entity_values("product"), None)
        if not product:
            dispatcher.utter_message(text="Which product are you checking stock for?")
            return []
        
        try:
            response = requests.get(f"{STOCK_API_URL}?product={product}", timeout=5)
            response.raise_for_status()
            stock_info = response.json().get("availability", "unknown")
            dispatcher.utter_message(text=f"Stock status for {product}: {stock_info}")
        except requests.exceptions.RequestException:
            dispatcher.utter_message(text="I couldn't check stock. Please try again later.")
        
        return []

class ActionCheckDelivery(Action):
    def name(self) -> Text:
        return "action_check_delivery"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        zipcode = next(tracker.get_latest_entity_values("zipcode"), None)

        if not zipcode:
            dispatcher.utter_message(text="Which ZIP code are you checking?")
            return []

        try:
            print("Checking zipcode {zipcode}") 
            response = requests.get(f"{DELIVERY_API_URL}{zipcode}", timeout=5)
            response.raise_for_status()
            data = response.json()
            #delivery_status = data.get("delivers", "unknown")
            dispatcher.utter_message(text=f"Delivery available: {data}")
        except requests.exceptions.RequestException:
            dispatcher.utter_message(text="I couldn't check delivery at the moment. Please try again later.")

        return []

class ActionFallbackOllama(Action):
    def name(self):
        return "action_fallback_ollama"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()

        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/generate",
                json={"model": "llama3.1", "prompt": f"You are Kevin, a pharmacy technician for CaryRx. Answer only pharmacy-related questions without giving drug advice. If the question is outside pharmacy, make up a plausible answer. You are based in Washington DC. {user_message}", "stream": False},
                timeout=10
            )
            response.raise_for_status()
            bot_response = response.json().get("response", "I couldn't generate a response.")
            dispatcher.utter_message(text=bot_response)
        except requests.exceptions.RequestException:
            dispatcher.utter_message(text="I couldn't process your request at the moment. Please try again later.")
        
        return []

