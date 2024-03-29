from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class ProfileManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().select_related('user')

    MALE = 'M'
    FEMALE = 'F'
    NA = 'N/A'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NA, 'N/A'),
    ]

    user = models.OneToOneField(
        User, related_name='customer', on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default=NA)
    profile_photo = models.ImageField(
        upload_to='images/profiles/', blank=True, null=True)

    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.last_name}- {self.user.first_name}'
