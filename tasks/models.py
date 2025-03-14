from django.db import models
from authentication.models import User

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name') 

    def __str__(self):
        return f"{self.name} :-({self.user.first_name} {self.user.last_name})"

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    estimated_time = models.PositiveIntegerField(help_text="Estimated time in minutes", default=0)
    time_spent = models.PositiveIntegerField(help_text="Time spent in minutes", default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_time_spent(self):
        total_time = self.sessions.aggregate(models.Sum('duration'))['duration__sum'] or 0
        self.time_spent = total_time
        self.save(update_fields=['time_spent'])

        
    def __str__(self):
        return self.title
    
            
class TaskSession(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="sessions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, help_text="Duration in minutes") 

    def calculate_duration(self):
        """Calculate session duration and store it in minutes."""
        if self.end_time:
            self.duration = (self.end_time - self.start_time).total_seconds() // 60
        else:
            self.duration = 0

    def save(self, *args, **kwargs):
        """Update duration and task time spent when a session is saved."""
        self.calculate_duration()
        super().save(*args, **kwargs)  
        self.task.update_time_spent() 

    def __str__(self):
        return f"Session for {self.task.title} by {self.user.first_name} {self.user.last_name}"
