from django.db import models

from app.region.models import Neighborhood, Farm, Massive, District
from app.users.models import User


class PickingType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SquadNumber(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)


class Squad(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='squads')
    squad_number = models.ForeignKey(SquadNumber, on_delete=models.SET_NULL, null=True, blank=True, related_name='squads')
    shtab = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='squads_as_shtab')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, null=True, blank=True)
    workers_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Otryad: {self.squad_number.number}"


class SquadExcelUpload(models.Model):
    file = models.FileField(upload_to="uploads/squad/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel: {self.file.name}"


class SquadDailyPicking(models.Model):
    class Status(models.TextChoices):
        active = "a", "active"
        finished = "f", "finished"

    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    massive = models.ForeignKey(Massive, on_delete=models.SET_NULL, null=True, blank=True)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.active)
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True, blank=True)
    masse = models.FloatField(null=True, blank=True)
    picking_type = models.ForeignKey(PickingType, on_delete=models.SET_NULL, null=True, blank=True)
    picked_area = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    workers_count = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.squad.squad_number)

    class Meta:
        ordering = ['-created_at', '-start_time']


class Worker(models.Model):
    squad = models.ForeignKey(Squad, on_delete=models.SET_NULL, blank=True, null=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    passport_id = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.full_name


class WorkerDailyPicking(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    masse = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.worker.full_name} - {self.masse} kg"


class Territory(models.Model):
    name = models.CharField(max_length=255)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, null=True, blank=True)
    picked_area = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name


class PQQM(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Scalesman(models.Model):
    pqqm = models.ForeignKey(PQQM, on_delete=models.SET_NULL, blank=True, null=True, related_name='pqqms')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    squad_number = models.ForeignKey(SquadNumber, on_delete=models.CASCADE)
    weight_checked = models.DecimalField(max_digits=20, decimal_places=2)
    tech_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tarozi #{self.pk}"


class CottonPicker(models.Model):
    car_number = models.IntegerField()
    hudud = models.ForeignKey(Territory, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Mashina {self.car_number}"


class CarDailyPicking(models.Model):
    cotton_picker = models.ForeignKey(CottonPicker, on_delete=models.CASCADE)
    fuel = models.FloatField()
    picked_area = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    cotton_masse = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.cotton_picker.car_number}"


class Shtab(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    massive = models.ForeignKey(Massive, on_delete=models.SET_NULL, null=True, blank=True)
    squad_number = models.ForeignKey(SquadNumber, on_delete=models.SET_NULL, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    picking_type = models.ForeignKey(PickingType, on_delete=models.SET_NULL, null=True, blank=True)
    number_pickers = models.IntegerField()
    workers_count = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Otryad: {self.squad_number}"
