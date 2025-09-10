from django.db import models
from django.conf import settings
from django.db.models.fields import CharField


class Region(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    plan = models.FloatField()
    crop_area = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class District(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    plan = models.FloatField()
    crop_area = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Massive(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    plan = models.FloatField()
    crop_area = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    massive = models.ForeignKey(Massive, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    crop_area = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Farm(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    massive = models.ForeignKey(Massive, on_delete=models.SET_NULL, blank=True, null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.SET_NULL, blank=True, null=True)
    massive_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    INN = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20)
    claster = models.CharField(max_length=255)
    cotton_area = models.FloatField()
    productivity = models.FloatField()
    gross_yield = models.FloatField()

    def __str__(self):
        return self.full_name


class FarmExcelUpload(models.Model):
    file = models.FileField(upload_to="uploads/farms/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel: {self.file.name}"
