from django.urls import path
from .views import (StateListView, SiteListView,
                     TaskListView,
                     ExcelUploadView, TaskSubmissionView,
                     ShiftPersonnelSubmissionView, ShiftDetailsView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload-excel/', ExcelUploadView.as_view(), name='upload-excel'),
    path('states/', StateListView.as_view(), name='state-list'),#Get all states
    path('sites/<int:state_id>/', SiteListView.as_view(), name='site-list'),#Get sites according to states
    path('tasks/<int:state_id>/<int:site_id>/<str:date>/<str:shift>/', TaskListView.as_view(), name='task-list'),#Get all tasks with machinery
    path('submit-report/', TaskSubmissionView.as_view(), name='submit-report'),
    path('submit-shift-personnel/', ShiftPersonnelSubmissionView.as_view(), name='submit-shift-personnel'),
    path('get-shift-details/<int:site_id>/<str:date>/<str:shift>/', ShiftDetailsView.as_view(), name='get-shift-details'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)