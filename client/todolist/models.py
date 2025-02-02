from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Site(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'state')

class ShiftData(models.Model):
    SHIFT_CHOICES = [(1, 'Shift 1'), (2, 'Shift 2')]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    description = models.TextField()
    shift = models.IntegerField(choices=SHIFT_CHOICES)
    date = models.DateField()
    machines = models.TextField()  # Comma-separated values
    people = models.TextField()    # Comma-separated values
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'shift']





class TaskIncompleteReport(models.Model):
    description = models.TextField(unique=True)
    reason = models.TextField()
    photo = models.ImageField(upload_to="uploads")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description
    
class TaskCompleteReport(models.Model):
    SHIFT_CHOICES = [(1, 'Shift 1'), (2, 'Shift 2')]
    description = models.TextField(unique=True)
    shift = models.IntegerField(choices=SHIFT_CHOICES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description
    
    
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
