from django.db import models
from django.conf import settings


class Region(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    plan = models.DecimalField(max_digits=20, decimal_places=2)
    crop_area = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class District(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    plan = models.DecimalField(max_digits=20, decimal_places=2)
    crop_area = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Massive(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    plan = models.DecimalField(max_digits=20, decimal_places=2)
    crop_area = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    massive = models.ForeignKey(Massive, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    crop_area = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Farm(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    massive = models.ForeignKey(Massive, on_delete=models.SET_NULL, blank=True, null=True)
    massive_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    INN = models.CharField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    claster = models.CharField(max_length=255)
    cotton_area = models.DecimalField(max_digits=20, decimal_places=2)
    productivity = models.DecimalField(max_digits=20, decimal_places=2)
    gross_yield = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.full_name


class FarmExcelUpload(models.Model):
    file = models.FileField(upload_to="uploads/farms/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel: {self.file.name}"
