# signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Task
from authentication.models import User
from django.db import transaction
from django.utils import timezone

@receiver(pre_save, sender=Task)
def update_user_points(sender, instance, **kwargs):
    try:
        previous_task = Task.objects.get(id=instance.id) 
    except Task.DoesNotExist:
        previous_task = None

    if previous_task:  
        # Check if the task's status has changed
        if previous_task.status != instance.status:
            if instance.status == 'completed':
                # Add 20 points when marking as completed
                instance.user.profile.points += 20
            elif previous_task.status == 'completed' and instance.status != 'completed':
                # Reduce 20 points when reverting a completed task to in_progress or todo
                instance.user.profile.points -= 20
            
            # Save the updated points for the user
            instance.user.save()



@receiver(post_save, sender=Task)
def update_user_streak(sender, instance, created, **kwargs):
    # Only proceed when the task is marked as 'completed' and has been updated (not created)
    if instance.status == 'completed':
        current_time = timezone.now()
        task_completed_on_time = False

        # Check if the task was completed within the due date and estimated time
        if instance.due_date and current_time.date() <= instance.due_date and instance.time_spent <= instance.estimated_time:
            task_completed_on_time = True
        
        # Update the streak based on task completion status
        if task_completed_on_time:
            instance.user.profile.streak += 1
            if instance.user.profile.streak > instance.user.profile.highest_streak:
                instance.user.profile.highest_streak = instance.user.profile.streak
        else:
            instance.user.profile.streak = 0  
        
        # Save the user's streak data
        instance.user.profile.save()
