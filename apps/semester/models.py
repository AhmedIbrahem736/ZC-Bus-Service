from django.db import models
from apps.base.models import CustomBaseModel

class Semester(CustomBaseModel):
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
    ]

    year = models.PositiveSmallIntegerField()
    semester_name = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    subscribe_valid_from = models.DateField()
    subscribe_valid_to = models.DateField()

    class Meta:
        unique_together = ['year', 'semester_name']

    def __str__(self):
        return f"{self.semester_name} {self.year}"
