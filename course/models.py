from django.db import models
from department.models import Department


class Course(models.Model):
    department = models.ForeignKey(
        Department, related_name='department_courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    acronym = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.acronym + " " + self.name
