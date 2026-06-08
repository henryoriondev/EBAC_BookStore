from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True,null=True)
    price = models.PositiveBigIntegerField(null=True)
    active = models.BooleanField(default=True)
    category = models.ManyToManyField('Category', blank=True)
    