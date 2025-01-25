from celery import shared_task
from django.core.mail import send_mail
from .models import WasteData

@shared_task
def send_bin_full_notification(bin_id):
    # Get the bin object
    bin = Bin.objects.get(bin_id=bin_id)
    # Get the latest waste data for the bin
    latest_waste_data = WasteData.objects.filter(bin=bin).latest('timestamp')
    # Check if the bin is full or nearing capacity
    if latest_waste_data.fill_level >= 0.9:  # Adjust the threshold as needed
        # Send an email notification to the bin owner
        subject = 'Your bin is full!'
        message = f'Your bin with ID {bin_id} is full or nearing capacity. Please empty it soon.'
        from_email = 'your_email@example.com'
        recipient_list = [bin.user.email]
        send_mail(subject, message, from_email, recipient_list)