from django.urls import path
from .views import (
    TaskListCreateAPI,
    TaskDetailAPI,
    task_list_view,
    task_add_view,
    task_edit_view
)

urlpatterns = [
    # REST API
    path("api/tasks/", TaskListCreateAPI.as_view()),
    path("api/tasks/<int:pk>/", TaskDetailAPI.as_view()),

    # UI screens
    path("", task_list_view, name="task_list"),
    path("add/", task_add_view, name="task_add"),
    path("edit/<int:pk>/", task_edit_view, name="task_edit"),
]
