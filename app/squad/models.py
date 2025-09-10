from django.db import models

from app.region.models import Neighborhood, Farm
from app.users.models import User


class Squad(models.Model):
    class PickingType(models.TextChoices):
        first = 'f', 'first'
        second = 's', 'second'
        third = 't', 'third'
        fourth = 'fr', 'fourth'

    squad_number = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    picking_type = models.CharField(max_length=100, choices=PickingType.choices)
    workers_count = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Otryad: {self.squad_number}"


class SquadDailyPicking(models.Model):
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)
    masse = models.FloatField()
    picked_area = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.squad.squad_number


class Worker(models.Model):
    squad = models.ForeignKey(Squad, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    passport_id = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=13)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class WorkerDailyPicking(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    masse = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.worker.full_name} - {self.masse} kg"


class Territory(models.Model):  # hudud
    name = models.CharField(max_length=255)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)
    picked_area = models.FloatField()

    def __str__(self):
        return self.name


class Scalesman(models.Model):  # tarozi
    pqqm_id = models.IntegerField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    squad_number = models.ForeignKey(Squad, on_delete=models.CASCADE)
    weight_checked = models.FloatField()
    tech_number = models.CharField(max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        return f"Tarozi #{self.pk}"


class CottonPicker(models.Model):  # terim mashinasi
    car_number = models.IntegerField()
    hudud = models.ForeignKey(Territory, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Mashina {self.car_number}"


class CarDailyPicking(models.Model):
    cotton_picker = models.ForeignKey(CottonPicker, on_delete=models.CASCADE)
    fuel = models.FloatField()
    picked_area = models.FloatField()
    cotton_masse = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.cotton_picker.car_number}"

