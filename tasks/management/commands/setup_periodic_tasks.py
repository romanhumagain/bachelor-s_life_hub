# from django.core.management.base import BaseCommand
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# import json

# class Command(BaseCommand):
#     help = "Sets up periodic task for sending reminders"

#     def handle(self, *args, **kwargs):
#         schedule, created = IntervalSchedule.objects.get_or_create(
#             every=1,
#             period=IntervalSchedule.DAYS,
#         )

#         PeriodicTask.objects.update_or_create(
#             name="Daily Task Reminder",
#             defaults={
#                 'interval': schedule,
#                 'task': 'tasks.tasks_reminder.send_task_reminders',
#                 'args': json.dumps([]),
#             }
#         )
#         self.stdout.write(self.style.SUCCESS("Successfully scheduled task reminders!"))



# from django.core.management.base import BaseCommand
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# import json

# class Command(BaseCommand):
#     help = "Sets up periodic task for sending dummy emails every 5 minutes"

#     def handle(self, *args, **kwargs):
#         # Create an interval schedule for 5 minutes
#         schedule, created = IntervalSchedule.objects.get_or_create(
#             every=5,  # Every 5 minutes
#             period=IntervalSchedule.MINUTES,  # Specify minutes
#         )

#         # Set up the periodic task for sending the dummy email
#         PeriodicTask.objects.update_or_create(
#             name="Dummy Email Reminder",  # Name of the task
#             defaults={
#                 'interval': schedule,  # Link the schedule
#                 'task': 'tasks.tasks_reminder.send_dummy_email',  # The task to run
#                 'args': json.dumps([]),  # Arguments for the task, empty in this case
#             }
#         )

#         self.stdout.write(self.style.SUCCESS("Successfully scheduled the dummy email reminder every 5 minutes!"))
