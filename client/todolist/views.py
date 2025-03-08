from collections import defaultdict
from django.core.cache import cache
from datetime import date
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from .models import (State, Site, ShiftData, TaskStatus, IncompleteTaskEvidence, Headcount)
from .serializers import (
    StateSerializer,SiteSerializer, TaskCreateSerializer,HeadcountCreateSerializer, UserSerializer,
    TaskStatusResponseSerializer
)
from .utils import get_current_shift, process_list_field
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Helper Functions
def get_cache_key(site_id, suffix):
    current_date = date.today()
    current_shift = get_current_shift()
    return f'site_{site_id}:{current_date}:{current_shift}:{suffix}'

# State/Site Navigation APIs
class StateList(APIView):
    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)

class SiteList(APIView):
    def get(self, request, state_id):
        sites = Site.objects.filter(state_id=state_id)
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)


class ImportExcelView(APIView):
    def post(self, request):
        try:
            df = pd.read_excel(request.FILES['file'])
            
            df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y', errors='coerce')
            
            # Drop rows with invalid dates
            df = df[df['date'].notna()]
            
            
            required_columns = ['state', 'site', 'description', 
                               'shift', 'date', 'machines', 'people']
            
            # Validate Excel columns
            missing = set(required_columns) - set(df.columns)
            if missing:
                return Response({"error": f"Missing columns: {missing}"}, status=400)

            cache_updates = defaultdict(lambda: {
                'descriptions': [],
                'machines': set(),
                'people': set(),
                'site_id': None,
                'date': None,
                'shift': None
            })

            state_cache = {}
            site_cache = {}
            shift_data_objects = []

            for _, row in df.iterrows():
                try:
                    # Process state
                    state_name = str(row['state']).strip()
                    if not state_name:
                        continue
                        
                    if state_name not in state_cache:
                        state, _ = State.objects.get_or_create(name=state_name)
                        state_cache[state_name] = state
                    state = state_cache[state_name]

                    # Process site
                    site_name = str(row['site']).strip()
                    if not site_name:
                        continue
                        
                    site_key = (state.id, site_name)
                    if site_key not in site_cache:
                        site, _ = Site.objects.get_or_create(
                            name=site_name,
                            state=state
                        )
                        site_cache[site_key] = site
                    site = site_cache[site_key]

                    # Process description
                    description = str(row['description']).strip()
                    if not description:
                        continue

                    # Process machines and people
                    machines = process_list_field(str(row['machines']))
                    people = process_list_field(str(row['people']))

                    # Create ShiftData object
                    shift_data_objects.append(ShiftData(
                        site=site,
                        description=description,
                        shift=int(row['shift']),
                        date=row['date'].date(),
                        machines=",".join(machines),
                        people=",".join(people)
                    ))

                    # Prepare cache updates
                    cache_key = (site.id, str(row['date'].date()), int(row['shift']))
                    cache_entry = cache_updates[cache_key]
                    cache_entry['descriptions'].append(description)
                    cache_entry['machines'].update(machines)
                    cache_entry['people'].update(people)
                    cache_entry['site_id'] = site.id
                    cache_entry['date'] = str(row['date'].date())
                    cache_entry['shift'] = int(row['shift'])

                except Exception as e:
                    print(f"Error processing row {_}: {str(e)}")
                    continue

            # Bulk create and update caches
            if shift_data_objects:
                ShiftData.objects.bulk_create(shift_data_objects)
                
                for key in cache_updates:
                    data = cache_updates[key]
                    base_key = f"site_{data['site_id']}:{data['date']}:{data['shift']}"
                    
                    # Update descriptions
                    desc_key = f"{base_key}:descriptions"
                    existing_desc = cache.get(desc_key, [])
                    cache.set(desc_key, existing_desc + data['descriptions'], 30*24*60*60)
                    
                    # Update machines
                    machine_key = f"{base_key}:machines"
                    existing_machines = set(cache.get(machine_key, []))
                    existing_machines.update(data['machines'])
                    cache.set(machine_key, sorted(existing_machines), 30*24*60*60)
                    
                    # Update people
                    people_key = f"{base_key}:people"
                    existing_people = set(cache.get(people_key, []))
                    existing_people.update(data['people'])
                    cache.set(people_key, sorted(existing_people), 30*24*60*60)

            return Response({
                "message": f"Processed {len(shift_data_objects)} valid records",
                "states": len(state_cache),
                "sites": len(site_cache)
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class SiteShiftDataView(APIView):
    def get(self, request, site_id):
        current_date = date.today()
        current_shift = get_current_shift()
        cache_key = f"site_{site_id}:{current_date}:{current_shift}:descriptions"
        return Response({
            "site_id": site_id,
            "date": current_date,
            "shift": current_shift,
            "descriptions": cache.get(cache_key, [])
        })

class SiteMachinesView(APIView):
    def get(self, request, site_id):
        current_date = date.today()
        current_shift = get_current_shift()
        cache_key = f"site_{site_id}:{current_date}:{current_shift}:machines"
        return Response({
            "site_id": site_id,
            "date": current_date,
            "shift": current_shift,
            "machines": cache.get(cache_key, [])
        })

class SitePeopleView(APIView):
    def get(self, request, site_id):
        current_date = date.today()
        current_shift = get_current_shift()
        cache_key = f"site_{site_id}:{current_date}:{current_shift}:people"
        return Response({
            "site_id": site_id,
            "date": current_date,
            "shift": current_shift,
            "people": cache.get(cache_key, [])
        })
        
        
# class TaskStatusView(APIView):
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#     def post(self, request):
#         serializer = TaskCreateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)
        
#         try:
#             shift_data = ShiftData.objects.get(id=serializer.validated_data['shift_data_id'])
#         except ShiftData.DoesNotExist:
#             return Response({"error": "Shift data not found"}, status=404)

#         # Create task status
#         task_status = TaskStatus.objects.create(
#             shift_data=shift_data,
#             description=serializer.validated_data['description'],
#             status=serializer.validated_data['status']
#         )

#         # Handle incomplete task evidence
#         if serializer.validated_data['status'] == 'incomplete':
#             required_fields = ['image', 'latitude', 'longitude']
#             missing_fields = [f for f in required_fields if f not in serializer.validated_data]
#             if missing_fields:
#                 return Response({
#                     "error": f"Missing fields for incomplete task: {', '.join(missing_fields)}"
#             }, status=400)
#             IncompleteTaskEvidence.objects.create(
#                 task_status=task_status,
#                 image=serializer.validated_data['image'],
#                 latitude=serializer.validated_data['latitude'],
#                 longitude=serializer.validated_data['longitude'],
#                 notes=serializer.validated_data.get('notes', '')
#             )

#         return Response({"message": "Task status recorded"}, status=201)

# class EnhancedShiftDataView(APIView):
#     def get(self, request, site_id):
#         current_date = date.today()
#         current_shift = get_current_shift()
        
#         # Get original shift data
#         cache_key = f"site_{site_id}:{current_date}:{current_shift}:descriptions"
#         descriptions = cache.get(cache_key, [])
        
#         # Get task statuses
#         task_statuses = TaskStatus.objects.filter(
#             shift_data__site_id=site_id,
#             shift_data__date=current_date,
#             shift_data__shift=current_shift
#         ).select_related('incompletetaskevidence')
        
#         # Serialize data
#         status_data = []
#         for status in task_statuses:
#             entry = {
#                 'description': status.description,
#                 'status': status.status,
#                 'timestamp': status.created_at
#             }
#             if status.status == 'incomplete':
#                 evidence = status.incompletetaskevidence
#                 entry.update({
#                     'image_url': request.build_absolute_uri(evidence.image.url),
#                     'coordinates': {
#                         'lat': float(evidence.latitude),
#                         'lng': float(evidence.longitude)
#                     },
#                     'notes': evidence.notes
#                 })
#             status_data.append(entry)
        
#         return Response({
#             "descriptions": descriptions,
#             "task_statuses": status_data
#         })
        
        
class TaskStatusView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        """
        Create a new task status with optional evidence for incomplete tasks.
        """
        serializer = TaskCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            shift_data = ShiftData.objects.get(id=serializer.validated_data['shift_data_id'])
        except ShiftData.DoesNotExist:
            return Response({"error": "Shift data not found"}, status=404)

        # Create task status
        task_status = TaskStatus.objects.create(
            shift_data=shift_data,
            description=serializer.validated_data['description'],
            status=serializer.validated_data['status']
        )

        # Handle incomplete task evidence
        if serializer.validated_data['status'] == 'incomplete':
            required_fields = ['image', 'latitude', 'longitude']
            missing_fields = [f for f in required_fields if f not in serializer.validated_data]
            if missing_fields:
                task_status.delete()  # Clean up if validation fails
                return Response({
                    "error": f"Missing fields for incomplete task: {', '.join(missing_fields)}"
                }, status=400)

            IncompleteTaskEvidence.objects.create(
                task_status=task_status,
                image=serializer.validated_data['image'],
                latitude=serializer.validated_data['latitude'],
                longitude=serializer.validated_data['longitude'],
                notes=serializer.validated_data.get('notes', '')
            )

        # Return the created task status with complete data
        response_serializer = TaskStatusResponseSerializer(task_status)
        return Response(response_serializer.data, status=201)

class EnhancedShiftDataView(APIView):
    def get(self, request, site_id):
        """
        Get enhanced shift data including task statuses and descriptions.
        """
        current_date = date.today()
        current_shift = get_current_shift()

        # Get original shift data from cache
        cache_key = f"site_{site_id}:{current_date}:{current_shift}:descriptions"
        descriptions = cache.get(cache_key, [])

        # Fetch all task statuses related to the site, avoiding filtering by date/shift
        task_statuses = TaskStatus.objects.filter(
            shift_data__site_id=site_id,
            # shift_data__date=current_date,
            # shift_data__shift=current_shift
        ).select_related('shift_data', 'incompletetaskevidence')

        # Use serializer for consistent data format
        status_serializer = TaskStatusResponseSerializer(task_statuses, many=True)
        
        # Format the response
        response_data = {
            "descriptions": descriptions,
            "task_statuses": status_serializer.data
        }

        return Response(response_data)

        
class HeadcountView(APIView):
    def post(self, request):
        serializer = HeadcountCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        try:
            site = Site.objects.get(id=serializer.validated_data['site_id'])
        except Site.DoesNotExist:
            return Response({"error": "Site not found"}, status=404)

        # Default to current date and shift if not provided
        date = serializer.validated_data.get('date') or timezone.now().date()
        shift = serializer.validated_data.get('shift') or get_current_shift()

        # Create or update headcount
        obj, created = Headcount.objects.update_or_create(
            site=site,
            person_name=serializer.validated_data['person_name'].strip(),
            date=date,
            shift=shift,
            defaults={'count': serializer.validated_data['count']}
        )

        return Response({
            "message": "Headcount updated" if not created else "Headcount created",
            "count": obj.count
        }, status=201)

    def get(self, request, site_id):
        # Get parameters with defaults
        req_date = request.query_params.get('date', str(timezone.now().date()))
        shift = request.query_params.get('shift', get_current_shift())
        
        try:
            site = Site.objects.get(id=site_id)
            headcounts = Headcount.objects.filter(
                site=site,
                date=req_date,
                shift=shift
            )
            
            structured_headcounts = []
            result = {}
        
            # First aggregate the counts
            for h in headcounts:
                result[h.person_name] = result.get(h.person_name, 0) + h.count
        
            # Convert to structured format
            for person_name, count in result.items():
                structured_headcounts.append({ 
                    "name": person_name,
                    "count": count,
                })
            
            return Response({
                "site_id": site_id,
                "site_name": site.name,  # Assuming site has a name field
                "date": req_date,
                "shift": shift,
                "headcounts": structured_headcounts
            })
        
        except Site.DoesNotExist:
            return Response({"error": "Site not found"}, status=404)
        
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)