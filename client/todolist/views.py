from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.utils import timezone
import io
from .models import Task, Site
from .serializers import TaskSerializer, TaskCompleteReportSerializer, TaskIncompleteReportSerializer


class ImportTasksView(APIView):
    def post(self, request):
        try:
            excel_file = request.FILES.get('excel_file')
            site_id = request.data.get('site_id')
            
            if not excel_file or not site_id:
                return Response(
                    {'error': 'Both excel_file and site_id are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            site = get_object_or_404(Site, id=site_id)
            df = pd.read_excel(excel_file)
            
            tasks = []
            for _, row in df.iterrows():
                task = Task(
                    site=site,
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
            
class TaskListView(APIView):
    def get(self, request, site_id):
        tasks = Task.objects.filter(site_id=site_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
class TaskCompleteView(APIView):
    def post(self, request, task_id):
        serializers = TaskCompleteReportSerializer(data = request.data)
        if not serializers.is_valid():
            return Response({'status': 403, 'message': 'Something went wrong'})
        serializers.save()
        return Response({'status': 200, 'message': 'Data Recieve'})
    
class TaskIncompleteView(APIView):
    def post(self, request, task_id):
        serializers = TaskIncompleteReportSerializer(data = request.data)
        if not serializers.is_valid():
            return Response({'status': 403, 'message': 'Something went wrong'})
        serializers.save()
        return Response({'status': 200, 'message': 'Data Recieve'})
    

# class TaskUpdateView(APIView):
#     def post(self, request, task_id):
#         task = get_object_or_404(Task, id=task_id)
#         action = request.data.get('action')
        
#         if action == 'complete':
#             task.mark_complete()
#             return Response({'message': 'Task marked as complete'})
        
#         elif action == 'incomplete':
#             reason = request.data.get('reason')
#             photo = request.FILES.get('photo')
            
#             if not reason or not photo:
#                 return Response(
#                     {'error': 'Both reason and photo are required'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             task.mark_incomplete()
#             TaskIncompleteReport.objects.create(
#                 task=task,
#                 reason=reason,
#                 photo=photo
#             )
            
#             return Response({'message': 'Task marked as incomplete with report'})
        
#         return Response(
#             {'error': 'Invalid action'},
#             status=status.HTTP_400_BAD_REQUEST
#         )
        
class DailyReportPDFView(APIView):
    def get(self, request, site_id):
        site = get_object_or_404(Site, id=site_id)
        today = timezone.now().date()
        tasks = Task.objects.filter(
            site=site,
            created_at__date=today
        )
        
        # Create PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Add content to PDF
        p.drawString(100, 750, f"Daily Report - {site.name}")
        p.drawString(100, 700, f"Date: {today}")
        
        y_position = 650
        for task in tasks:
            p.drawString(120, y_position, f"Task: {task.description}")
            p.drawString(120, y_position-20, f"Status: {task.status}")
            
            if task.status == 'incomplete':
                report = task.incomplete_reports.first()
                if report:
                    p.drawString(140, y_position-40, f"Reason: {report.reason}")
            
            y_position -= 100
        
        p.showPage()
        p.save()
        buffer.seek(0)
        
        # Create response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=daily_report_{today}.pdf'
        response.write(buffer.getvalue())
        buffer.close()
        
        return response