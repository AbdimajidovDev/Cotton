# from django.contrib import admin
# from django.contrib.admin import StackedInline
#
# from app.squad.models import *
#
#
# class SquadDailyPickingAdmin(StackedInline):
#     model = SquadDailyPicking
#     extra = 1
#
# @admin.register(Squad)
# class SquadAdmin(admin.ModelAdmin):
#     list_display = ('squad_number', 'user', 'neighborhood', 'farm', 'picking_type', 'workers_count')
#     inlines = (SquadDailyPickingAdmin,)
#
#
# # @admin.register(SquadDailyPicking)
# # class SquadDailyPickingAdmin(admin.ModelAdmin):
# #     model = SquadDailyPicking


from django.contrib import admin
from django.contrib.admin import StackedInline

from app.squad.models import (
    Squad, SquadDailyPicking, Worker, WorkerDailyPicking,
    Territory, Scalesman, CottonPicker, CarDailyPicking,
    Shtab, PickingType, SquadNumber, PQQM
)


# ========================= Inline Admins =========================

class SquadDailyPickingInline(StackedInline):
    model = SquadDailyPicking
    extra = 1


class WorkerInline(StackedInline):
    model = Worker
    extra = 1


class WorkerDailyPickingInline(StackedInline):
    model = WorkerDailyPicking
    extra = 1


class TerritoryInline(StackedInline):
    model = Territory
    extra = 1


class ScalesmanInline(StackedInline):
    model = Scalesman
    extra = 1


class CottonPickerInline(StackedInline):
    model = CottonPicker
    extra = 1


class CarDailyPickingInline(StackedInline):
    model = CarDailyPicking
    extra = 1


# ========================= Main Admins =========================

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ("squad_number", "user", "neighborhood", "picking_type", "workers_count")
    search_fields = ("squad_number__number", "user__first_name", "user__last_name")
    list_filter = ("picking_type", "neighborhood")
    inlines = [SquadDailyPickingInline, WorkerInline, TerritoryInline]


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "passport_id", "phone_number", "squad", "is_active")
    search_fields = ("full_name", "passport_id", "phone_number")
    list_filter = ("is_active", "squad")
    inlines = [WorkerDailyPickingInline]


@admin.register(Territory)
class TerritoryAdmin(admin.ModelAdmin):
    list_display = ("name", "squad", "picked_area")
    inlines = [CottonPickerInline]


@admin.register(CottonPicker)
class CottonPickerAdmin(admin.ModelAdmin):
    list_display = ("car_number", "hudud", "farm", "created_at")
    inlines = [CarDailyPickingInline]


@admin.register(Shtab)
class ShtabAdmin(admin.ModelAdmin):
    list_display = ("squad_number", "farm", "massive", "picking_type", "workers_count", "created_at")
    search_fields = ("squad_number__number",)


@admin.register(PickingType)
class PickingTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(SquadNumber)
class SquadNumberAdmin(admin.ModelAdmin):
    list_display = ("number",)


@admin.register(PQQM)
class PQQMAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Scalesman)
class ScalesmanAdmin(admin.ModelAdmin):
    list_display = ("farm", "squad_number", "weight_checked", "tech_number", "created_at")
