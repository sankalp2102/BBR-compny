from django.urls import path
from .views import (
    StateList, SiteList,
    ImportExcelView,
    SiteShiftDataView, SiteMachinesView, SitePeopleView,
    TaskStatusView, EnhancedShiftDataView, HeadcountView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Data Import
    path('import/', ImportExcelView.as_view()),
    
    
    path('states/', StateList.as_view()),
    path('states/<int:state_id>/sites/', SiteList.as_view()),
    
    
    
    # Site-specific Data
    path('sites/<int:site_id>/shift-data/', SiteShiftDataView.as_view()),
    path('sites/<int:site_id>/machines/', SiteMachinesView.as_view()),
    path('sites/<int:site_id>/people/', SitePeopleView.as_view()),
    
    
    path('task-status/', TaskStatusView.as_view()),
    path('enhanced-shift-data/<int:site_id>/', EnhancedShiftDataView.as_view()),
    
    path('headcount/', HeadcountView.as_view()),  # POST
    path('sites/<int:site_id>/headcount/', HeadcountView.as_view()),  # GET
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)