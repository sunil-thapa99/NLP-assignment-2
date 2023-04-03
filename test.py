import requests
import streamlit as st

rasa_server_url = "http://localhost:5005"
webhook_url = f"{rasa_server_url}/webhooks/rest/webhook"

def send_message(message):
    parse_endpoint = f"{rasa_server_url}/model/parse"
    headers = {"Content-Type": "application/json"}

    # Send message to model/parse endpoint to get intent
    payload = {"text": message}
    response = requests.post(parse_endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        intent_name = response_data["intent"]["name"]

        # Send message and intent to Rasa webhook
        payload = {"sender": "user", "message": message, "intent": {"name": intent_name}}
        response = requests.post(webhook_url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data[0]["text"]
        else:
            return "Error connecting to webhook"
    else:
        return "Error connecting to model/parse"

def main():
    st.title("Rasa Streamlit Chatbot")
    st.markdown("Enter your message below:")

    message = st.text_input("Message")

    if message:
        bot_response = send_message(message)
        st.text_area("Bot Response", value=bot_response, height=200, max_chars=None)

if __name__ == "__main__":
    main()
