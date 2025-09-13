from rest_framework import serializers

from app.region.models import Region
from app.squad.models import Territory, Squad, Worker, CottonPicker

class TerritoryReportSerializer(serializers.ModelSerializer):
    plan = serializers.IntegerField(source="plan_amount")
    squads_count = serializers.SerializerMethodField()
    workers_count = serializers.SerializerMethodField()
    active_workers = serializers.SerializerMethodField()
    inactive_workers = serializers.SerializerMethodField()
    machines_count = serializers.SerializerMethodField()
    hand_picked_mass = serializers.SerializerMethodField()
    machine_picked_mass = serializers.SerializerMethodField()
    region_executed_plan = serializers.SerializerMethodField()
    region_unfulfilled_plan = serializers.SerializerMethodField()
    active_squad = serializers.SerializerMethodField()
    inactive_squad = serializers.SerializerMethodField()
    pickers_count = serializers.SerializerMethodField()
    active_pickers = serializers.SerializerMethodField()
    inactive_pickers = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            "id",
            "name",
            "plan",
            "region_executed_plan",
            "region_unfulfilled_plan",

            "squads_count",
            "active_squad",
            "inactive_squad",

            "pickers_count",
            "active_pickers",
            "inactive_pickers",

            "workers_count",
            "active_workers",
            "inactive_workers",

            "machines_count",

            "hand_picked_mass",
            "machine_picked_mass",
        ]

    # def get_squads_count(self, obj):
    #     return Squad.objects.filter(territory=obj).count()
    #
    # def get_workers_count(self, obj):
    #     return Worker.objects.filter(squad__territory=obj).count()
    #
    # def get_machines_count(self, obj):
    #     return CottonPicker.objects.filter(squad__territory=obj).count()

    # def get_hand_picked_mass(self, obj):
    #     from app.squad.models import WorkerDailyPicking
    #     return WorkerDailyPicking.objects.filter(
    #         worker__squad__territory=obj
    #     ).aggregate(total=models.Sum("mass"))["total"] or 0
    #
    # def get_machine_picked_mass(self, obj):
    #     from app.squad.models import CarDailyPicking
    #     return CarDailyPicking.objects.filter(
    #         squad__territory=obj
    #     ).aggregate(total=models.Sum("mass"))["total"] or 0
