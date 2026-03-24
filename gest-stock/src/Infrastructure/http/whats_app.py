from twilio.rest import Client
import random
import os
 
ACCOUNT_SID = "seu_account_sid_aqui"
AUTH_TOKEN = "seu_auth_token_aqui"
WHATSAPP_NUMBER = "whatsapp:+14155238886"  
 
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