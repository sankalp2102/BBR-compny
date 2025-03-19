from django.urls import path
from .views import (StateListView, SiteListView,
                     TaskListView,
                     ExcelUploadView, TaskSubmissionView,
                     ShiftPersonnelSubmissionView,UserRegisterView, 
                     QuantityCreateView, ReconcilationCreateView,
                     ShiftDetailsView, CompletedTasksListView,
                     IncompleteTasksListView)

from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version='v1',
        description="API documentation for task management system",
    ),
    public=True,
    authentication_classes=[],  # ✅ Remove authentication for Swagger UI
    permission_classes=[AllowAny],  # ✅ Make it publicly accessible
)

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'), 
    # Optional UI:
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    
    path('upload-excel/', ExcelUploadView.as_view(), name='upload-excel'),
    path('states/', StateListView.as_view(), name='state-list'),#Get all states
    path('sites/<int:state_id>/', SiteListView.as_view(), name='site-list'),#Get sites according to states
    path('tasks/<int:state_id>/<int:site_id>/<str:date>/<str:shift>/', TaskListView.as_view(), name='task-list'),#Get all tasks with machinery
    path('submit-report/', TaskSubmissionView.as_view(), name='submit-report'),
    path('submit-shift-personnel/', ShiftPersonnelSubmissionView.as_view(), name='submit-shift-personnel'),
    path('submit-quantity/',QuantityCreateView.as_view(),name='submit-quantity'),
    path('submit-reconciliation/',ReconcilationCreateView.as_view(),name='submit-reconciliation'),
    path('get-all-data/<int:site_id>/<str:date>/<str:shift>/', ShiftDetailsView.as_view(), name='get-all-data'),
    path('completed-tasks/<int:site_id>/<str:date>/<str:shift>/', CompletedTasksListView.as_view(), name='completed-tasks'),
    path('incomplete-tasks/<int:site_id>/', IncompleteTasksListView.as_view(), name='incomplete-tasks'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
