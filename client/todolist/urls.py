from django.urls import path
from .views import ImportTasksView, TaskListView, TaskUpdateView, DailyReportPDFView

urlpatterns = [
    path('import-tasks/', ImportTasksView.as_view(), name='import-tasks'),
    path('tasks/<int:site_id>/', TaskListView.as_view(), name='task-list'),
    path('task/<int:task_id>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('daily-report/<int:site_id>/', DailyReportPDFView.as_view(), name='daily-report'),
]
