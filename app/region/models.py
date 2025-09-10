from django.db import models
from django.conf import settings


class Region(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    plan = models.FloatField()
    crop_area = models.FloatField()
    farm = models.ForeignKey("Farm", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class District(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    plan = models.FloatField()
    crop_area = models.FloatField()
    farm = models.ForeignKey("Farm", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Massive(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    plan = models.FloatField()
    crop_area = models.FloatField()
    farm = models.ForeignKey("Farm", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    massive = models.ForeignKey(Massive, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    crop_area = models.FloatField()
    farm = models.ForeignKey("Farm", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Farm(models.Model):
    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    INN = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.full_name
