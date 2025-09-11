from django.contrib import admin
from django.contrib.admin import StackedInline

from app.squad.models import *


class SquadDailyPickingAdmin(StackedInline):
    model = SquadDailyPicking
    extra = 1

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ('squad_number', 'user', 'neighborhood', 'farm', 'picking_type', 'workers_count')
    inlines = (SquadDailyPickingAdmin,)


# @admin.register(SquadDailyPicking)
# class SquadDailyPickingAdmin(admin.ModelAdmin):
#     model = SquadDailyPicking
