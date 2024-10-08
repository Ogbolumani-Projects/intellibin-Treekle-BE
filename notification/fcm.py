from firebase_admin.messaging import Message, Notification, AndroidConfig, AndroidNotification, APNSConfig
from fcm_django.models import FCMDevice
from authservice.models import CustomUser

def send_message_to_device(user: CustomUser, title, body, image=None, data=None):
    try:
        device = FCMDevice.objects.get(user=user)
        send = device.send_message(Message(notification=Notification(
            title=title, body=body, image=image), data=data))
        print('Sent message to', device, '\nReturned:', send)
    except Exception as e:
        print(e, '\nCould not cloud send message to device')


def send_message_to_topic(topic_name, title, body, image=None, data=None):
    try:
        send = FCMDevice.send_topic_message(
            Message(notification=Notification(title=title, body=body, image=image), data=data), topic_name)
        print('Sent message to', topic_name, '\nReturned:', send)
    except Exception as e:
        print(e, '\nCould not cloud send message to topic')