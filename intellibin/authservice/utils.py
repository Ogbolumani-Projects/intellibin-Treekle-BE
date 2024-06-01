
from django.core.mail import send_mail
from pyotp import TOTP
import random
import time
import secrets

totp = TOTP('base32secret3232', interval=60)
def generate_otp():

    return totp.now()



def generate_otp():


def send_mail_to_user():