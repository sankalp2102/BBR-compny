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


class TaskStatus(models.Model):
    shift_data = models.ForeignKey(ShiftData, on_delete=models.CASCADE, related_name='task_statuses')
    description = models.TextField()  # Copy of original description
    status = models.CharField(max_length=20, choices=[
        ('completed', 'Completed'),
        ('incomplete', 'Incomplete')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.description}"

class IncompleteTaskEvidence(models.Model):
    task_status = models.OneToOneField(TaskStatus, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='task_evidence/')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Headcount(models.Model):
    SHIFT_CHOICES = [(1, 'Shift 1'), (2, 'Shift 2')]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)
    date = models.DateField()
    shift = models.IntegerField(choices=SHIFT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('site', 'person_name', 'date', 'shift')