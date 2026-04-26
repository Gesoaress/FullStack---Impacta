from twilio.rest import Client
from dotenv import load_dotenv
import random
import os

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

def generate_code():
    return str(random.randint(1000, 9999))

def send_whatsapp_code(phone, code):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=f"Seu código de ativação é: {code}",
        from_=WHATSAPP_NUMBER,
        to=f"whatsapp:{phone}"
    )
    return message.sid