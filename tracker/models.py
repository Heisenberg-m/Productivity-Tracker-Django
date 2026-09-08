from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Monday = models.FloatField(default=0)
    Tuesday = models.FloatField(default=0)
    Wednesday = models.FloatField(default=0)
    Thursday = models.FloatField(default=0)
    Friday = models.FloatField(default=0)
    Saturday = models.FloatField(default=0)
    Sunday = models.FloatField(default=0)

    def __str__(self):
        return f"Goal for {self.user.username}"

class LogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracker_logs')
    date = models.DateField()
    hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.hours} hrs)"