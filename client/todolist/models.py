from django.db import models

class Task(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description

class TaskIncompleteReport(models.Model):
    description = models.TextField(unique=True)
    reason = models.TextField()
    photo = models.URLField(max_length=100000)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description
    
class TaskCompleteReport(models.Model):
    description = models.TextField(unique=True)
    remark = models.TextField()
    completed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description
    
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
