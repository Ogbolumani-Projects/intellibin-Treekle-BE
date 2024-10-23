import requests
from django.conf import settings
from django.http import HttpResponse


PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY

def initialize_payment(email, amount):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "amount": amount
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

# Add a card - tokenization
# def add_card(request):
#     if request.method == 'POST':
#         card_number = request.POST['card_number']
#         exp_month = request.POST['exp_month']
#         exp_year = request.POST['exp_year']
#         cvv = request.POST['cvv']
        
#         # Send card details to Paystack API for tokenization
#         paystack_response = paystack_tokenize(card_number, exp_month, exp_year, cvv)
        
#         if paystack_response['status'] == 'success':
#             # Store the authorization token in the database
#             user_card = UserCard(user=request.user, authorization_code=paystack_response['data']['authorization_code'])
#             user_card.save()
#             return HttpResponse('Card added successfully')
#         else:
#             return HttpResponse('Error adding card')

# Charge the saved card
def charge_card(user, amount, authorization_code):
    payload = {
        'email': user.email,
        'amount': amount,  # in kobo
        'authorization_code': authorization_code
    }
    response = requests.post('https://api.paystack.co/transaction/charge_authorization', data=payload, headers={
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'
    })
    
    return response.json()
