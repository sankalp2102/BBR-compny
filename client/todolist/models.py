from django.db import models

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
    

class TaskIncompleteReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='incomplete_reports')
    reason = models.TextField()
    photo = models.ImageField(upload_to='task_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

class TaskCompleteReport(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='complete_reports')
    remark = models.TextField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
class PlantOnSite(models.Model):
    Name = models.TextField()
    
    def __str__(self):
        return self.Name
    
class PersonOnSite(models.Model):
    Name = models.TextField()
    
    def __str__(self):
        return self.Name
    
class PersonAttendaceRecord(models.Model):
    person = models.ForeignKey(
        PersonOnSite, 
        on_delete=models.CASCADE, 
        related_name='PersonName'  # Unique related_name
    )
    date = models.DateField(auto_now_add=True)
    Number = models.IntegerField()
    def __str__(self):
        return f"{self.person.Name} - {self.date}"


class PlantAttendance(models.Model):
    machine = models.ForeignKey(
        PlantOnSite, 
        on_delete=models.CASCADE, 
        related_name='MachineryName'  # Unique related_name
    )
    date = models.DateField(auto_now_add=True)
    Number = models.IntegerField()
    def __str__(self):
        return f"{self.machine.Name} - {self.date}"
