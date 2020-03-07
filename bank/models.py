from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    balance = models.FloatField()
    killer = models.BooleanField(default=False)
    alive = models.BooleanField(default=True)
    test = models.BooleanField(default=False)