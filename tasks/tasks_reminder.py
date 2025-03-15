from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Task
from django.conf import settings

@shared_task
def send_task_reminders():
    """Sends reminder emails for tasks due tomorrow."""
    tomorrow = now().date() + timedelta(days=1)
    tasks = Task.objects.filter(due_date=tomorrow)

    for task in tasks:
        subject = f"Reminder: Your task '{task.title}' is due tomorrow!"
        message = f"Hello {task.user.first_name} {task.user.last_name},\n\nYour task '{task.title}' is due tomorrow ({task.due_date}). Please complete it on time.\n\nBest Regards,\nTask Manager"
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  
            [task.user.email],
            fail_silently=False,
        )

    return f"Sent reminders for {tasks.count()} tasks."




@shared_task
def send_dummy_email():
  
    """Sends a dummy email message for testing every 5 minutes."""
    subject = "Test Email"
    message = "This is a dummy email sent every 5 minutes for testing purposes."
    recipient_list = ['romanhumagain69@gmail.com']  # This email should be set in your settings.py for testing purposes

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Your email host user
        recipient_list,
        fail_silently=False,
    )
    return "Dummy email sent successfully."