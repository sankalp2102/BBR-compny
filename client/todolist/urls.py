from django.urls import path
from .views import TaskCompleteView, TaskIncompleteView,PersonAttendanceView, PlantAttendanceView, StateList, SiteList, ImportExcelView, SiteShiftDataView, SiteMachinesView, SitePeopleView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # Navigation
    path('states/', StateList.as_view()),
    path('states/<int:state_id>/sites/', SiteList.as_view()),
    
    # Data Import
    path('import/', ImportExcelView.as_view()),
    
    
    # Site-specific Data
    path('sites/<int:site_id>/shift-data/', SiteShiftDataView.as_view()),
    path('sites/<int:site_id>/machines/', SiteMachinesView.as_view()),
    path('sites/<int:site_id>/people/', SitePeopleView.as_view()),
    
    
    
    
    path('completedtask/<int:site_id>/', TaskCompleteView.as_view(), name= 'Completed-task'),#working
    path('incompletedtask/<int:site_id>/', TaskIncompleteView.as_view(), name= 'Incomplete-task'),#working
    path('post-people/<int:site_id>/', PersonAttendanceView.as_view(), name='Post_people'),#working
    path('post-plant/<int:site_id>/', PlantAttendanceView.as_view(), name='No_of_plant'),#working
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)