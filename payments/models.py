from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Order(models.Model):
    status = models.CharField(max_length=255, default='pending')
    amount = models.FloatField(default=10.0)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

