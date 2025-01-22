from django.db import models

class Task(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class TaskIncompleteReport(models.Model):
    description = models.TextField(default='')
    reason = models.TextField()
    photo = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class TaskCompleteReport(models.Model):
    description = models.TextField()
    remark = models.TextField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
class PlantOnSite(models.Model):
    Name = models.TextField()
    
    def __str__(self):
        return self.Name
    
class PersonOnSite(models.Model):
    Name = models.TextField()
    
    def __str__(self):
        return self.Name
    
class PersonAttendaceRecord(models.Model):
    Name = models.TextField()
    date = models.DateField(auto_now_add=True)
    Number = models.IntegerField()
    def __str__(self):
        return self.Name


class PlantAttendance(models.Model):
    Name = models.TextField()
    date = models.DateField(auto_now_add=True)
    Number = models.IntegerField()
    def __str__(self):
        return self.Name
