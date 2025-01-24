from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .models import Task, PersonOnSite, PlantOnSite, TaskCompleteReport, TaskIncompleteReport
from .serializers import TaskSerializer, TaskCompleteReportSerializer, TaskIncompleteReportSerializer, PersonOnSiteSerializer, PlantOnSiteSerializer, PersonOnSiteNameSerializer, PlantOnSiteNameSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class ImportTasksView(APIView):
    def post(self, request):
        try:
            excel_file = request.FILES.get('excel_file')
            
            if not excel_file :
                return Response(
                    {'error': 'Excel_file required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            df = pd.read_excel(excel_file)
            
            tasks = []
            for _, row in df.iterrows():
                task = Task(
                
                    description=row['task_description']  # Adjust column name as per your Excel sheet
                )
                tasks.append(task)
            
            Task.objects.bulk_create(tasks)
            
            return Response({'message': 'Tasks imported successfully'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
            
            
class TaskListView(APIView): #get all the Task from backend
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    
    
    
class TaskCompleteView(APIView):
    def post(self, request):
        serializers = TaskCompleteReportSerializer(data = request.data)
        if not serializers.is_valid():
            return Response({'status': 403, 'message': 'Something went wrong'})
        serializers.save()
        return Response({'status': 200, 'message': 'Data Recieve'})
    
    def get(self, request):
        tasks = TaskCompleteReport.objects.all()
        serializers = TaskCompleteReportSerializer(tasks, many=True)
        return Response(serializers.data)
    
    
    
    
    
    
    
class TaskIncompleteView(APIView): #Incompleted task send to backend
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        serializers = TaskIncompleteReportSerializer(data = request.data)
        if not serializers.is_valid():
            return Response({'status': 403, 'message': 'Something went wrong'})
        serializers.save()
        return Response({'status': 200, 'message': 'Data Recieve'})
        
    def get(self, request):
        tasks = TaskIncompleteReport.objects.all()
        serializers = TaskIncompleteReportSerializer(tasks, many=True)
        return Response(serializers.data)    
    

        
        
class PersonAttendanceView(APIView): #Send number of people prenset on site
    def post(self, request):
        serializers = PersonOnSiteSerializer(data = request.data)
        if not serializers.is_valid():
            return Response({'status': 403, 'message': 'Something went wrong'})
        serializers.save()
        return Response({'status': 200, 'message': 'Data Recieve'})
    
class PersonNameView(APIView): #Get Name of persons on site
    def get(self, request):
        persons = PersonOnSite.objects.all()
        serializer = PersonOnSiteNameSerializer(persons, many=True)
        return Response(serializer.data)
    



    
class PlantAttendanceView(APIView): #Send number of Machine prenset on site
    def post(self, request):
        serializers = PlantOnSiteSerializer(data = request.data)
        if not serializers.is_valid():
            return Response({'status': 403, 'message': 'Something went wrong'})
        serializers.save()
        return Response({'status': 200, 'message': 'Data Recieve'})

class PlantNameView(APIView): #Get Name of persons on site
    def get(self, request):
        persons = PlantOnSite.objects.all()
        serializer = PlantOnSiteNameSerializer(persons, many=True)
        return Response(serializer.data)
    