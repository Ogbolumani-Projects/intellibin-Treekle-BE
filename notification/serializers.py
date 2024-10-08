import firebase_admin
from firebase_admin import messaging

def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )
    
    try:
        response = messaging.send(message)
        return {'status': 'success', 'response': response}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
    
    