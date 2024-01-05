# models.py in myapp
from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=100)
    other_field1 = models.CharField(max_length=100)
    other_field2 = models.CharField(max_length=100)

class Response(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)
