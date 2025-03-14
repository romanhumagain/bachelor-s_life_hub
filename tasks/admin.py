from django.contrib import admin
from .models import Tag,  Task, TaskSession

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(TaskSession)
