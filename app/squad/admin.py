from django.contrib import admin

from app.squad.models import *


@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ('squad_number', 'user', 'neighborhood', 'farm', 'picking_type', 'workers_count')


@admin.register(SquadDailyPicking)
class SquadDailyPickingAdmin(admin.ModelAdmin):
    model = SquadDailyPicking
