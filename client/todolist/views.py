from rest_framework.generics import ListAPIView, CreateAPIView
from .models import State, Site, Shift, Task, Machinery, TaskStatus, TaskReport, ReasonForDelay, ShiftSummary, Quantity
from .serializers import StateSerializer, SiteSerializer, TaskSerializer, UserRegisterSerializer, ShiftSummarySerializer, QuantitySerializer
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import AllowAny, BasePermission 
from django.utils.timezone import now
from geopy.geocoders import Nominatim 
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import re
from datetime import datetime


User = get_user_model()

class UserRegisterView(CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # ✅ No authentication needed to register
    
class IsOfficeOrCEO(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Office', 'CEO']
    #Put this in any function to get to make sure the user is authenticated and has the role of Office or CEO
    #permission_classes = [IsOfficeOrCEO]
    #Similar for other roles also

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

            # Regex pattern to extract machinery name and time
            pattern = r"([\w\s]+)\((\d{2}:\d{2})-(\d{2}:\d{2})\)"

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

                # Process machinery using regex
                machinery_data = str(row['Machinery'])
                machinery_objects = []

                matches = re.findall(pattern, machinery_data)

                if not matches:
                    return Response({"error": f"Invalid machinery format at row {index + 2}"}, status=status.HTTP_400_BAD_REQUEST)

                for match in matches:
                    machinery_name, time_from_str, time_to_str = match

                    # Convert time strings to time objects
                    try:
                        time_from = datetime.strptime(time_from_str, "%H:%M").time()
                        time_to = datetime.strptime(time_to_str, "%H:%M").time()
                    except ValueError:
                        return Response({"error": f"Invalid time format at row {index + 2}"}, status=status.HTTP_400_BAD_REQUEST)

                    # Ensure machinery exists
                    machinery, _ = Machinery.objects.get_or_create(
                        name=machinery_name,
                        defaults={'time_from': time_from_str, 'time_to': time_to_str}
                    )

                    # Update time if necessary
                    machinery.time_from = time_from_str
                    machinery.time_to = time_to_str
                    machinery.save()

                    machinery_objects.append(machinery)

                # Assign machinery to the task
                task.machinery.set(machinery_objects)

            return Response({"message": "Data imported successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class TaskSubmissionView(APIView):

    def post(self, request):
        """
        API to handle task submission based on its status.
        """


        site_id = request.data.get("site_id")  
        date = request.data.get("date")  
        shift_name = request.data.get("shift")  
        task_id = request.data.get("task")
        task_name = request.data.get("task_name")
        type_of_work = request.data.get("type_of_work")
        status_choice = request.data.get("status")  # Complete / Incomplete / Partially Complete
        personnel_engaged = request.data.get("personnel_engaged", [])  
        machinery_used = request.data.get("machinery_used", [])  
        equipment_used = request.data.get("equipment_used", [])  
        personnel_idled = request.data.get("personnel_idled", [])  
        equipment_idled = request.data.get("equipment_idled", [])  
        reason_for_delay = request.data.get("reason_for_delay", {})
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        photo = request.FILES.get("photo")

        try:

            site = Site.objects.filter(id=site_id).first()
            if not site:
                return Response({"error": "Invalid Site ID"}, status=status.HTTP_400_BAD_REQUEST)


            shift = Shift.objects.filter(site=site, date=date, shift=shift_name).first()
            if not shift:
                return Response({"error": "Invalid Shift for the given Site and Date"}, status=status.HTTP_400_BAD_REQUEST)


            if task_id:
                task = Task.objects.filter(id=task_id, shift=shift).first()
            elif task_name:
                task = Task.objects.filter(name=task_name, shift=shift).first()
            
            if not task:
                return Response({"error": "Task does not exist for this shift"}, status=status.HTTP_400_BAD_REQUEST)
            
            if type_of_work:
                task.type_of_work = type_of_work
                task.save()


            task_status = TaskStatus.objects.create(task=task, status=status_choice, timestamp=now())


            task_report = TaskReport.objects.create(
                task_status=task_status,
                personnel_engaged=personnel_engaged,
                machinery_used=machinery_used,  
                equipment_used=equipment_used,
                personnel_idled=personnel_idled,
                equipment_idled=equipment_idled
            )


            if status_choice in ["Incomplete", "Partially Complete"] and reason_for_delay:

                location_name = "Unknown Location"
                if latitude and longitude:
                    geolocator = Nominatim(user_agent="geoapiExercises")
                    try:
                        location_data = geolocator.reverse((latitude, longitude), exactly_one=True)
                        location_name = location_data.address if location_data else "Unknown Location"
                    except Exception:
                        location_name = "Error retrieving location"


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

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ShiftPersonnelSubmissionView(generics.CreateAPIView):
    queryset = ShiftSummary.objects.all()
    serializer_class = ShiftSummarySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Submit Shift Personnel Data",
        request=ShiftSummarySerializer,
        responses={201: ShiftSummarySerializer, 400: "Bad Request", 500: "Internal Server Error"},
    )
    def create(self, request, *args, **kwargs):
        site_id = request.data.get("site_id")
        shift_name = request.data.get("shift")
        date = request.data.get("date")
        personnel_list = request.data.get("personnel_list", [])

        try:
            site = Site.objects.get(id=site_id)
            shift = Shift.objects.filter(site=site, date=date, shift=shift_name).first()
            if not shift:
                return Response({"error": "Shift not found for the given site and date"}, status=status.HTTP_400_BAD_REQUEST)

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

class ShiftDetailsView(APIView):
    def get(self, request, site_id, date, shift):
        """
        GET API to retrieve all tasks, machinery, task reports, personnel, 
        task completion status, and quantity data for a specific site, date, and shift.
        """

        # Ensure shift exists for the given site & date
        shift_obj = Shift.objects.filter(site_id=site_id, date=date, shift=shift).first()
        if not shift_obj:
            return Response({"error": "Shift not found for the given site and date"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all tasks for this shift
        tasks = Task.objects.filter(shift=shift_obj)

        # Retrieve quantity data for this shift
        quantities = Quantity.objects.filter(shift=shift_obj)
        quantity_data = [
            {"material_name": q.material_name, "quantity": q.quantity}
            for q in quantities
        ]

        # Prepare response data
        shift_details = {
            "site_id": site_id,
            "date": date,
            "shift": shift,
            "tasks": [],
            "quantities": quantity_data
        }

        # Loop through each task and get related reports
        for task in tasks:
            task_status = TaskStatus.objects.filter(task=task).first()
            task_report = TaskReport.objects.filter(task_status=task_status).first()
            reason_for_delay = ReasonForDelay.objects.filter(task_report=task_report).first()

            task_data = {
                "task_id": task.id,
                "task_name": task.name,
                "status": task_status.status if task_status else "Not Reported",
                "machinery_needed": list(task.machinery.all().values_list("name", flat=True)),
                "report": {
                    "personnel_engaged": task_report.personnel_engaged if task_report else [],
                    "machinery_used": task_report.machinery_used if task_report else [],
                    "equipment_used": task_report.equipment_used if task_report else [],
                    "personnel_idled": task_report.personnel_idled if task_report else [],
                    "equipment_idled": task_report.equipment_idled if task_report else [],
                    "reason_for_delay": {
                        "reason": reason_for_delay.reason if reason_for_delay else None,
                        "details": reason_for_delay.details if reason_for_delay else None,
                        "location": reason_for_delay.location if reason_for_delay else None,
                        "photo": reason_for_delay.photo.url if reason_for_delay and reason_for_delay.photo else None,
                        "time_reported": reason_for_delay.time_reported if reason_for_delay else None
                    } if reason_for_delay else None
                }
            }

            shift_details["tasks"].append(task_data)

        # Get personnel list for the shift
        shift_summary = ShiftSummary.objects.filter(site_id=site_id, shift=shift_obj, date=date).first()
        shift_details["personnel_list"] = shift_summary.personnel_list if shift_summary else []

        return Response(shift_details, status=status.HTTP_200_OK)
    

class QuantityCreateView(generics.CreateAPIView):
    serializer_class = QuantitySerializer

    def create(self, request, *args, **kwargs):
        site_id = request.data.get('site_id')
        date = request.data.get('date')
        shift_name = request.data.get('shift')
        materials_data = request.data.get('materials', [])

        # Validate required fields
        if not (site_id and date and shift_name and materials_data):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if Site and Shift exist using site_id
            try:
                site = Site.objects.get(id=site_id)
                shift = Shift.objects.get(site=site, date=date, shift=shift_name)
            except (Site.DoesNotExist, Shift.DoesNotExist):
                return Response({"error": "Site or Shift not found"}, status=status.HTTP_404_NOT_FOUND)

            # Save quantities
            for material in materials_data:
                material_name = material.get('material_name')
                quantity = material.get('quantity')

                if not material_name or quantity is None:
                    return Response({"error": "Invalid material data"}, status=status.HTTP_400_BAD_REQUEST)

                # Save to Quantity model
                Quantity.objects.create(
                    shift=shift,
                    material_name=material_name,
                    quantity=quantity
                )

            return Response({"message": "Quantities added successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
