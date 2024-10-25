import requests
from django.conf import settings
from django.http import HttpResponse

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY

def initialize_payment(email, amount, callback_url):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "amount": int(amount) * 100,
        "callback_url": callback_url,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def verify_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Charge the saved card
def charge_card(user, amount, authorization_code):
    payload = {
        'email': user.email,
        'amount': int(amount) * 100,  # in kobo
        'authorization_code': authorization_code
    }
    response = requests.post('https://api.paystack.co/transaction/charge_authorization', data=payload, headers={
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'
    })
    
    return response.json()
