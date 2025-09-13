from rest_framework import serializers
from .models import Squad, SquadDailyPicking, Worker, WorkerDailyPicking, Territory, Scalesman, CottonPicker, \
    CarDailyPicking, PickingType
from ..region.models import Farm, District, Massive
from django.utils import timezone
from datetime import datetime


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
    district = serializers.SerializerMethodField()
    massive = serializers.SerializerMethodField()

    class Meta:
        model = SquadDailyPicking
        fields = [
            "id", "squad", "status", "farm", "district", "massive",
            "masse", "picking_type", "picked_area", "workers_count",
            "start_time", "end_time", "created_at"
        ]
        read_only_fields = ["created_at", "start_time", "end_time"]

    def get_farm(self, obj):
        return obj.farm.full_name if obj.farm else None

    def get_district(self, obj):
        return obj.farm.district.name if obj.farm and obj.farm.district else None

    def get_massive(self, obj):
        return obj.farm.massive.name if obj.farm and obj.farm.massive else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['squad_number'] = (
            instance.squad.squad_number.number if instance.squad.squad_number else None
        )
        return data


class StartSquadDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = SquadDailyPicking
        fields = ["workers_count", "farm", "picking_type", "squad"]
        read_only_fields = ["start_time", "end_time", "created_at", "status", "squad"]

    def create(self, validated_data):
        validated_data["status"] = SquadDailyPicking.Status.active
        farm = validated_data.get("farm")
        if farm:
            validated_data["district"] = farm.district
            validated_data["massive"] = farm.massive
        return super().create(validated_data)


class EndSquadDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = SquadDailyPicking
        fields = ["picked_area", "masse"]
        read_only_fields = ["start_time", "end_time", "created_at", "status"]

    def update(self, instance, validated_data):
        farm = instance.farm
        if farm:
            instance.district = farm.district
            instance.massive = farm.massive
        return super().update(instance, validated_data)


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


class SquadForShtabSerializer(serializers.ModelSerializer):
    squad_number = serializers.SerializerMethodField()
    user_full_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Squad
        fields = ["id", "squad_number", "user_full_name"]

    def get_squad_number(self, obj):
        return obj.squad_number.number if obj.squad_number else None


class ShtabSquadDailyCreateSerializer(serializers.ModelSerializer):
    squad_number = serializers.IntegerField(write_only=True)
    date = serializers.DateField(write_only=True)
    picking_type = serializers.PrimaryKeyRelatedField(queryset=PickingType.objects.all())

    class Meta:
        model = SquadDailyPicking
        fields = [
            "id", "squad_number", "date",
            "farm", "picking_type", "workers_count",
            "start_time", "end_time", "status"
        ]
        read_only_fields = ["id", "start_time", "end_time"]

    def create(self, validated_data):
        squad_number = validated_data.pop("squad_number")
        date = validated_data.pop("date")

        try:
            squad = Squad.objects.get(squad_number__number=squad_number)
        except Squad.DoesNotExist:
            raise serializers.ValidationError({"squad_number": "Bunday squad mavjud emas"})

        now_time = timezone.localtime().time()
        start_dt = timezone.make_aware(
            datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=now_time.hour,
                minute=now_time.minute,
                second=now_time.second
            )
        )

        validated_data["start_time"] = start_dt
        validated_data["squad"] = squad
        validated_data["status"] = SquadDailyPicking.Status.active

        farm = validated_data.get("farm")
        if farm:
            validated_data["district"] = farm.district
            validated_data["massive"] = farm.massive

        return SquadDailyPicking.objects.create(**validated_data)
