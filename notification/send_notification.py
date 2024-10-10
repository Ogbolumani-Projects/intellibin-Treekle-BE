from authservice.models import CustomUser
from .fcm import send_message_to_device, send_message_to_topic
from .models import Notification

def send_notification_to_user(user, title, msg):
    # create notification
    Notification.objects.create(user=user, title=title, msg=msg, recipient="User")

    # send push notification
    send_message_to_device(user, title, msg)

def send_message_to_admin(title, msg):
    # Get all admins and create notification
    admins = CustomUser.objects.filter(is_admin=True)
    for admin in admins:
        Notification.objects.create(user=admin, title=title, msg=msg, recipient="Admin")

    # send push notification
    send_message_to_topic("Admin", title, msg)
    