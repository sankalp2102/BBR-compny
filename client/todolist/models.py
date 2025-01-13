from django.db import models
from django.utils import timezone

class Site(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('incomplete', 'Incomplete')
    ]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def mark_complete(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_incomplete(self):
        self.status = 'incomplete'
        self.completed_at = None
        self.save()

class TaskIncompleteReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='incomplete_reports')
    reason = models.TextField()
    photo = models.ImageField(upload_to='task_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
