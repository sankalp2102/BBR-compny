from django.urls import path
from .views import ImportTasksView, TaskListView, TaskCompleteView, TaskIncompleteView, PlantNameView, PersonNameView, PersonAttendanceView, PlantAttendanceView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('import-tasks/', ImportTasksView.as_view(), name='import-tasks'),#reject for now
    path('tasks/', TaskListView.as_view(), name='task-list'),#working
    path('completedtask/', TaskCompleteView.as_view(), name= 'Completed-task'),#working
    path('incompletedtask/', TaskIncompleteView.as_view(), name= 'Incomplete-task'),#working
    path('get-person-name/', PersonNameView.as_view(), name='Person_name'),#working
    path('get-plant-name/', PlantNameView.as_view(), name='Plant_name'),#working
    path('post-people/', PersonAttendanceView.as_view(), name='Post_people'),#working
    path('post-plant/', PlantAttendanceView.as_view(), name='No_of_plant'),#working
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)