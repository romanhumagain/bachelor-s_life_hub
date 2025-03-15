from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .models import Task

@shared_task
def send_task_reminder_emails():
    try:
        # Calculate tomorrow's date
        tomorrow = timezone.now().date() + timedelta(days=1)

        # Get all tasks due tomorrow
        due_tasks = Task.objects.filter(due_date=tomorrow, status__in=['todo', 'in_progress'])

        # Group tasks by user
        user_tasks = {}
        for task in due_tasks:
            if task.user.email not in user_tasks:
                user_tasks[task.user.email] = []
            user_tasks[task.user.email].append(task)

        # Send emails to each user
        for user_email, tasks in user_tasks.items():
            try:
                task_list = "\n".join([f"- {task.title} (Priority: {task.priority})" for task in tasks])

                subject = f"Task Reminder: You have {len(tasks)} task(s) due tomorrow"
                message = f"""Hello,

                            This is a friendly reminder that you have the following task(s) due tomorrow:

                            {task_list}

                            Please log in to your account to manage these tasks.

                            Best regards,
                            Bachelor's Life Hub
                            """

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send email to {user_email}: {e}")

        return f"Sent reminders for {len(due_tasks)} tasks to {len(user_tasks)} users"

    except Exception as e:
        print(f"Error in send_task_reminder_emails task: {e}")
        return "Failed to send task reminders due to an error."