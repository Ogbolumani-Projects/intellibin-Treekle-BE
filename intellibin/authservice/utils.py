from django.core.mail import send_mail
from pyotp import TOTP

totp = TOTP('base32secret3232', interval=120)
def generate_otp():

    return totp.now()

def send_mail_to_user(user_mail):
    try:
        mail = send_mail(
            subject="OTP Verification for wastebin",
            from_email="the.ayoadeborah@gmail.com",
            recipient_list=[user_mail],
            message=generate_otp()
        )
    except Exception as e:
        print(e)