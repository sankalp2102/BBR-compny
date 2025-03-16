from django.db import models
from django.contrib.auth.models import AbstractUser

class State(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Site(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Shift(models.Model):
    SHIFT_CHOICES = [('Day', 'Day'), ('Night', 'Night')]

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)

    def __str__(self):
        return f"{self.site.name} - {self.date} - {self.shift}"

class Machinery(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    machinery = models.ManyToManyField(Machinery, related_name="tasks")  # Allow multiple machinery

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    STATUS_CHOICES = [
        ('Complete', 'Complete'),
        ('Incomplete', 'Incomplete'),
        ('Partially Complete', 'Partially Complete'),
    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.name} - {self.status}"


class TaskReport(models.Model):
    task_status = models.OneToOneField(TaskStatus, on_delete=models.CASCADE)
    personnel_engaged = models.JSONField(default=list)  # Stores role + count
    machinery_used = models.JSONField(default=list)  # ✅ Store machinery as text list
    equipment_used = models.JSONField(default=list)  # ✅ Store equipment as text list
    personnel_idled = models.JSONField(default=list, blank=True, null=True)  
    equipment_idled = models.JSONField(default=list, blank=True, null=True)  

    def __str__(self):
        return f"Report for {self.task_status.task.name} ({self.task_status.status})"


class ReasonForDelay(models.Model):
    task_report = models.ForeignKey(TaskReport, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    details = models.TextField()
    photo = models.ImageField(upload_to='media/', blank=True, null=True)  # Save image
    location = models.CharField(max_length=255, blank=True, null=True)  # Converted location
    latitude = models.FloatField(blank=True, null=True)  # Store latitude
    longitude = models.FloatField(blank=True, null=True)  # Store longitude
    time_reported = models.DateTimeField(auto_now_add=True)  # Time of image upload

    def __str__(self):
        return f"Delay for {self.task_report.task_status.task.name} - {self.reason}"

class ShiftSummary(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)  # ✅ Link to Site
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)  # ✅ Link to Shift
    personnel_list = models.JSONField(default=list)  # ✅ Store personnel count
    date = models.DateField()  # ✅ Store date separately

    def __str__(self):
        return f"Shift Summary - {self.site.name} - {self.shift.shift} ({self.date})"
    
USER_ROLES = (
    ('CEO', 'CEO'),
    ('Office', 'Office'),
    ('Technician', 'Technician'),
)

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='Technician')

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # ✅ Fix the conflict with auth.User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # ✅ Fix the conflict with auth.User
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"
