from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, Tag, TaskSession
from .serializers import TaskSerializer, TagSerializer, DetailedTagSerializer
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
from rest_framework.views import APIView
from django.utils.timezone import now
from .serializers import TaskSerializer
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        priority_order = Case(
            When(priority='high', then=Value(1)),
            When(priority='medium', then=Value(2)),
            When(priority='low', then=Value(3)),
            default=Value(4),
            output_field=IntegerField()
        )

        return Task.objects.filter(user=self.request.user).order_by('due_date', priority_order)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        task_count = Task.objects.filter(user=request.user).count()
        completed_task_count = Task.objects.filter(user=request.user, status='completed').count()
        points = getattr(request.user.profile, 'points', 0)  
        today = now().date()
        
        context = {
            'total_task_count': task_count,
            'completed_task_count': completed_task_count, 
            'points': points,   
        }
        
        return Response(context, status=status.HTTP_200_OK)
    
    
class KanbanBoardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
       
        points = request.user.profile.points
        todo_tasks = Task.objects.filter(user=request.user, status='todo') .order_by('due_date', 'priority') 
        in_progress_tasks = Task.objects.filter(user=request.user, status='in_progress').order_by('due_date', 'priority')  
        completed_tasks = Task.objects.filter(user=request.user, status='completed').order_by('due_date', 'priority')

        # Serialize the tasks
        todo_serializer = TaskSerializer(todo_tasks, many=True)
        in_progress_serializer = TaskSerializer(in_progress_tasks, many=True)
        completed_serializer = TaskSerializer(completed_tasks, many=True)

        # Prepare the response context
        context = {
            'points':points,
            'todo_tasks': todo_serializer.data,
            'in_progress_tasks': in_progress_serializer.data,
            'completed_tasks': completed_serializer.data,
        }

        return Response(context, status=status.HTTP_200_OK)


class TagListView(APIView):
    def get(self, request):
        """Fetch all tags with their total tasks and completed tasks."""
        tags = Tag.objects.filter(user = request.user)
        serializer = DetailedTagSerializer(tags, many=True)
        return Response(serializer.data)
    

class StartTimerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        user = request.user 
        
        if TaskSession.objects.filter(task=task, user=user, end_time__isnull=True).exists():
            return Response({"error": "A session is already running"}, status=status.HTTP_400_BAD_REQUEST)

        session = TaskSession(task=task, user=user, start_time=timezone.now())
        session.save()

        return Response(
            {
                "message": "Timer started.",
                "session_id": session.id,
                "start_time": session.start_time,
                "total_time_spent": task.time_spent,
            },
            status=status.HTTP_201_CREATED
        )
        
class StopTimerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, session_id):
        try:
            session = TaskSession.objects.get(id=session_id, user=request.user, end_time__isnull=True)
            session.end_time = timezone.now()
            session.save()

            return Response(
                {
                    "message": "Timer stopped.",
                    "session_id": session.id,
                    "duration": session.duration,
                    "total_time_spent": session.task.time_spent,
                },
                status=status.HTTP_200_OK
            )
        except TaskSession.DoesNotExist:
            return Response({"error": "No active session found"}, status=status.HTTP_400_BAD_REQUEST)

class CancelTimerSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        
        try:
            session = TaskSession.objects.get(id=session_id, user=request.user)
            session.delete()
        
            return Response({"message": "Timer session canceled successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except TaskSession.DoesNotExist:
            return Response({"error": "Session not found or you don't have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)