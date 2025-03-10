from django.urls import path, re_path
from .views import (StateListView, SiteListView,
                     TaskListView,
                     ExcelUploadView, TaskSubmissionView,
                     ShiftPersonnelSubmissionView, ShiftDetailsView,
                     UserRegisterView)

from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version='v1',
        description="API documentation for task management system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="developer@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    authentication_classes=[],  # ✅ Remove authentication for Swagger UI
    permission_classes=[AllowAny],  # ✅ Make it publicly accessible
)

urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    
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