from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TagViewSet, StartTimerAPIView, StopTimerAPIView, CancelTimerSessionAPIView,  TagListView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:task_id>/start-timer-session/', StartTimerAPIView.as_view(), name='start-task-timer'),
    path('<int:session_id>/save-timer-session/', StopTimerAPIView.as_view(), name='stop-task-timer'),
    path('milestones/', TagListView.as_view(), name='tag-list'),
    path('cancel-timer-session/<int:session_id>/', CancelTimerSessionAPIView.as_view(), name='cancel-timer'),
]
