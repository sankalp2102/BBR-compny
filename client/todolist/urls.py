from django.urls import path
from .views import ImportTasksView, TaskListView, DailyReportPDFView, TaskCompleteView, TaskIncompleteView

urlpatterns = [
    path('import-tasks/', ImportTasksView.as_view(), name='import-tasks'),
    path('tasks/<int:site_id>/', TaskListView.as_view(), name='task-list'),
    path('Completedtask/<int:task_id>/', TaskCompleteView.as_view(), name= 'Completed-task'),
    path('incompletedtask/<int:task_id>/', TaskIncompleteView.as_view(), name= 'Incomplete-task'),
    path('daily-report/<int:site_id>/', DailyReportPDFView.as_view(), name='daily-report'),
]