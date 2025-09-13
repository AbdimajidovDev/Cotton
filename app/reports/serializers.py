from rest_framework import serializers
from django.db.models import Sum, Count, Q

from app.region.models import Region
from app.squad.models import Worker, CottonPicker, WorkerDailyPicking, CarDailyPicking, Squad


class RegionReportSerializer(serializers.ModelSerializer):
    plan = serializers.SerializerMethodField()

    # Squad stats
    squads_count = serializers.SerializerMethodField()
    active_squads = serializers.SerializerMethodField()
    inactive_squads = serializers.SerializerMethodField()

    # Worker stats
    pickers_count = serializers.SerializerMethodField()
    active_pickers = serializers.SerializerMethodField()
    inactive_pickers = serializers.SerializerMethodField()

    # Machine stats
    machines_count = serializers.SerializerMethodField()
    active_machines = serializers.SerializerMethodField()
    inactive_machines = serializers.SerializerMethodField()

    # Picking mass
    hand_picked_mass = serializers.SerializerMethodField()
    machine_picked_mass = serializers.SerializerMethodField()

    # Plan execution
    executed_plan = serializers.SerializerMethodField()
    unfulfilled_plan = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            "id", "name", "plan",
            "executed_plan", "unfulfilled_plan",
            "squads_count", "active_squads", "inactive_squads",
            "pickers_count", "active_pickers", "inactive_pickers",
            "machines_count", "active_machines", "inactive_machines",
            "hand_picked_mass", "machine_picked_mass",
        ]


    def get_plan(self, obj):
        return obj.plan

    # ---------------- Squad stats ----------------
    def get_squads_count(self, obj):
        return Squad.objects.filter(
            neighborhood__massive__district__region=obj
        ).count()

    def get_active_squads(self, obj):
        return Squad.objects.filter(
            neighborhood__massive__district__region=obj,
        ).count()

    def get_inactive_squads(self, obj):
        return self.get_squads_count(obj) - self.get_active_squads(obj)

    # ---------------- Worker stats ----------------
    def get_pickers_count(self, obj):
        return Worker.objects.filter(
            squad__neighborhood__massive__district__region=obj
        ).count()

    def get_active_pickers(self, obj):
        return Worker.objects.filter(
            squad__neighborhood__massive__district__region=obj,
            is_active=True
        ).count()

    def get_inactive_pickers(self, obj):
        return self.get_pickers_count(obj) - self.get_active_pickers(obj)

    # ---------------- Machine stats ----------------
    def get_machines_count(self, obj):
        return CottonPicker.objects.filter(
            car_dailies_picking__farm__region=obj
        ).distinct().count()

    def get_active_machines(self, obj):
        return CottonPicker.objects.filter(
            car_dailies_picking__farm__region=obj,
            user__is_active=True
        ).distinct().count()

    def get_inactive_machines(self, obj):
        return self.get_machines_count(obj) - self.get_active_machines(obj)

    # ---------------- Picking mass ----------------
    def get_hand_picked_mass(self, obj):
        return WorkerDailyPicking.objects.filter(
            worker__squad__neighborhood__massive__district__region=obj
        ).aggregate(total_mass=Sum('masse'))['total_mass'] or 0

    def get_machine_picked_mass(self, obj):
        return CarDailyPicking.objects.filter(
            farm__region=obj
        ).aggregate(total_mass=Sum('cotton_masse'))['total_mass'] or 0

    # ---------------- Plan execution ----------------
    def get_executed_plan(self, obj):
        return self.get_hand_picked_mass(obj) + self.get_machine_picked_mass(obj)

    def get_unfulfilled_plan(self, obj):
        return max(obj.plan - self.get_executed_plan(obj), 0)
