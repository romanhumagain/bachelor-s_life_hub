from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from tasks.views import DashboardAPIView, KanbanBoardAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('authentication.urls') ),
    path('api/task/', include('tasks.urls') ),
    path('api/dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    path('api/kanban-board/', KanbanBoardAPIView.as_view(), name='kanban-board'),
    

    
    
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
