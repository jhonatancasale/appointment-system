from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextField


class Appointment(models.Model):
    date = models.DateField()
    start_at = models.TimeField()
    end_at = models.TimeField()

    patient = models.ForeignKey(User, on_delete=models.PROTECT)
    procedure: TextField = models.TextField()

    def __str__(self):
        return '{date!r}, [{start_at!r} - {end_at!r}] - {patient!r}'.format(
            date=str(self.date),
            start_at=self.start_at.strftime("%H:%M"),
            end_at=self.end_at.strftime("%H:%M"),
            patient=self.patient.username
        )
