from rest_framework import serializers
from .models import Squad, SquadDailyPicking, Worker, WorkerDailyPicking, Territory, Scalesman, CottonPicker, \
    CarDailyPicking


class SquadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squad
        fields = '__all__'
        read_only_fields = ('created_at',)


class SquadDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = SquadDailyPicking
        fields = '__all__'
        read_only_fields = ["start_time", "end_time", "created_at"]


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'


class WorkerDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerDailyPicking
        fields = '__all__'


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = '__all__'


class ScalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scalesman
        fields = '__all__'


class CottonPickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottonPicker
        fields = '__all__'
        read_only_fields = ('created_at',)


class CarDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDailyPicking
        fields = '__all__'
