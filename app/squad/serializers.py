from rest_framework import serializers
from .models import Squad, SquadDailyPicking, Worker, WorkerDailyPicking, Territory, Scalesman, CottonPicker, \
    CarDailyPicking
from ..region.models import Farm, District, Massive


class SquadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squad
        fields = '__all__'
        read_only_fields = ('created_at',)


class FarmMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['full_name']


class DistrictMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['name']


class MassiveMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massive
        fields = ['name']


class SquadNestedSerializer(serializers.ModelSerializer):
    squad_number = serializers.IntegerField(source='squad.squad_number.number')

    class Meta:
        model = SquadDailyPicking
        fields = ['squad_number']


class SquadDailySerializer(serializers.ModelSerializer):
    farm = serializers.SerializerMethodField()
    district = DistrictMinimalSerializer(read_only=True)
    massive = MassiveMinimalSerializer(read_only=True)

    class Meta:
        model = SquadDailyPicking
        fields = [
            "id", "squad", "status", "farm", "district", "massive",
            "masse", "picking_type", "picked_area", "workers_count",
            "start_time", "end_time", "created_at"
        ]
        read_only_fields = ["created_at", "start_time", "end_time"]

    def get_farm(self, obj):
        # agar farm mavjud bo'lsa full_name qaytaradi
        return obj.farm.full_name if obj.farm else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['squad_number'] = (
            instance.squad.squad_number.number if instance.squad.squad_number else None
        )
        return data



class StartSquadDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = SquadDailyPicking
        fields = ["workers_count", "farm", "picking_type"]
        read_only_fields = ["start_time", "end_time", "created_at", "status"]


class EndSquadDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = SquadDailyPicking
        fields = ["picked_area", "masse"]
        read_only_fields = ["start_time", "end_time", "created_at", "status"]


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
