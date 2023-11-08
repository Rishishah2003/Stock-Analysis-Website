from django.db import models

# Create your models here.
class Stock(models.Model):
    stockticker = models.CharField(max_length=200)
    stockname = models.CharField(max_length=200)