from rest_framework import serializers
from .models import Task, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'status',
            'priority', 'estimated_time', 'time_spent', 'tags', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])

        # Create the task instance
        task = Task.objects.create(**validated_data)

        # Handle tags
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(user=task.user, name=tag_data['name'])
            task.tags.add(tag)  # Add tag to the task

        return task

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        # Update the task fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags_data is not None:
            instance.tags.clear()  # Clear existing tags
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(user=instance.user, name=tag_data['name'])
                instance.tags.add(tag)  # Add the new tags

        instance.save()
        return instance


class DetailedTagSerializer(serializers.ModelSerializer):
    total_tasks = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    # tasks = TaskSerializer(many=True, read_only=True) 

    class Meta:
        model = Tag
        fields = ['id', 'name', 'total_tasks', 'completed_tasks', 'is_completed']

    def get_total_tasks(self, obj):
        return obj.tasks.count()

    def get_completed_tasks(self, obj):
        return obj.tasks.filter(status='completed').count()
    
    def get_is_completed(self, obj):
        return  obj.tasks.count() == obj.tasks.filter(status='completed').count()
    
    