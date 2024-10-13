from typing import Iterable
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    images = models.JSONField(default=list, blank=True)
    description = models.TextField(default='', blank=True)

    added_on = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False, help_text='Visible to other users')
    added_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='courses')

    def __str__(self) -> str:
        return self.name


class Hole(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='holes')

    number = models.PositiveSmallIntegerField()
    distance = models.PositiveBigIntegerField(help_text='Distance from the tee to the hole in yards')
    par = models.PositiveSmallIntegerField(help_text='Number of strokes a golfer should take to complete the hole')

    class Meta:
        unique_together = ('course', 'number')

    def __str__(self) -> str:
        return f'{self.course.name} #{self.number}'
