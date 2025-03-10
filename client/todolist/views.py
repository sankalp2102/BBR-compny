from rest_framework.generics import ListAPIView, CreateAPIView
from .models import State, Site, Shift, Task, Machinery, TaskStatus, TaskReport, ReasonForDelay, ShiftSummary
from .serializers import StateSerializer, SiteSerializer, TaskSerializer, TaskStatusSerializer, TaskReportSerializer, ReasonForDelaySerializer, ShiftSummarySerializer
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.utils.timezone import now
from geopy.geocoders import Nominatim 
class StateListView(ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class SiteListView(ListAPIView):
    serializer_class = SiteSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        return Site.objects.filter(state_id=state_id)

class TaskListView(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        state_id = self.kwargs['state_id']
        site_id = self.kwargs['site_id']
        date = self.kwargs['date']
        shift = self.kwargs['shift']

        try:
            shift_obj = Shift.objects.get(site_id=site_id, date=date, shift=shift)
            return Task.objects.filter(shift=shift_obj).prefetch_related('machinery')
        except Shift.DoesNotExist:
            return Task.objects.none()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No tasks found for the given filters"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExcelUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                # Ensure state exists
                state, _ = State.objects.get_or_create(name=row['State'])

                # Ensure site exists
                site, _ = Site.objects.get_or_create(state=state, name=row['Site'])

                # Ensure shift exists
                shift, _ = Shift.objects.get_or_create(
                    site=site,
                    date=row['Date'],
                    shift=row['Shift']
                )

                # Ensure task exists
                task, _ = Task.objects.get_or_create(
                    shift=shift,
                    name=row['Task']
                )

                # Ensure machinery exists separately
                machinery_list = [m.strip() for m in str(row['Machinery']).split(",")]
                machinery_objects = []
                for machinery_name in machinery_list:
                    machinery, _ = Machinery.objects.get_or_create(name=machinery_name)
                    machinery_objects.append(machinery)

                # Assign machinery to the task
                task.machinery.set(machinery_objects)  # ✅ Correct Many-to-Many assignment

            return Response({"message": "Data imported successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskSubmissionView(APIView):
    def post(self, request):
        """
        API to handle task submission based on its status.
        """

        # Extracting data from request
        task_id = request.data.get("task")
        task_name = request.data.get("task_name")
        status_choice = request.data.get("status")  # Complete / Incomplete / Partially Complete
        personnel_engaged = request.data.get("personnel_engaged", [])  
        machinery_used = request.data.get("machinery_used", [])  # ✅ Text List (not IDs)
        equipment_used = request.data.get("equipment_used", [])  
        personnel_idled = request.data.get("personnel_idled", [])  
        equipment_idled = request.data.get("equipment_idled", [])  
        reason_for_delay = request.data.get("reason_for_delay", {})
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        photo = request.FILES.get("photo")

        try:
            # Fetch task by ID or Name
            if task_id:
                task = Task.objects.get(id=task_id)
            elif task_name:
                task = Task.objects.filter(name=task_name).first()
                if not task:
                    return Response({"error": "Task name does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Either task_id or task_name must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Create TaskStatus Entry
            task_status = TaskStatus.objects.create(task=task, status=status_choice, timestamp=now())

            # Create TaskReport Entry
            task_report = TaskReport.objects.create(
                task_status=task_status,
                personnel_engaged=personnel_engaged,
                machinery_used=machinery_used,  # ✅ Now stored as text list
                equipment_used=equipment_used,
                personnel_idled=personnel_idled,
                equipment_idled=equipment_idled
            )

            # Handle Incomplete or Partially Complete reasons
            if status_choice in ["Incomplete", "Partially Complete"] and reason_for_delay:
                # Convert Coordinates to Location
                location_name = "Unknown Location"
                if latitude and longitude:
                    geolocator = Nominatim(user_agent="geoapiExercises")
                    try:
                        location_data = geolocator.reverse((latitude, longitude), exactly_one=True)
                        location_name = location_data.address if location_data else "Unknown Location"
                    except Exception:
                        location_name = "Error retrieving location"

                # Save Delay Details
                ReasonForDelay.objects.create(
                    task_report=task_report,
                    reason=reason_for_delay.get("reason"),
                    details=reason_for_delay.get("details"),
                    latitude=latitude,
                    longitude=longitude,
                    location=location_name,
                    time_reported=now(),
                    photo=photo
                )

            return Response({"message": "Task report submitted successfully!"}, status=status.HTTP_201_CREATED)

        except Task.DoesNotExist:
            return Response({"error": "Invalid Task ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ShiftPersonnelSubmissionView(APIView):
    def post(self, request):
        """
        API to handle personnel submission for a given site, shift, and date.
        """

        # Extracting data from request
        site_id = request.data.get("site_id")
        shift_name = request.data.get("shift")  # "Day" or "Night"
        date = request.data.get("date")  # Format: YYYY-MM-DD
        personnel_list = request.data.get("personnel_list", [])  # List of {role, count}

        try:
            # Validate site
            site = Site.objects.get(id=site_id)

            # Validate shift
            shift = Shift.objects.filter(site=site, date=date, shift=shift_name).first()
            if not shift:
                return Response({"error": "Shift not found for the given site and date"}, status=status.HTTP_400_BAD_REQUEST)

            # Create or Update Shift Summary
            shift_summary, created = ShiftSummary.objects.update_or_create(
                site=site, shift=shift, date=date,
                defaults={"personnel_list": personnel_list}
            )

            return Response(
                {"message": "Shift personnel data submitted successfully!", "shift_summary_id": shift_summary.id},
                status=status.HTTP_201_CREATED
            )

        except Site.DoesNotExist:
            return Response({"error": "Invalid Site ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)