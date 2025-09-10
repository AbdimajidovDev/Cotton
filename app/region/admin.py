from django.contrib import admin
from .models import Region, District, Massive, Neighborhood, Farm


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "plan", "crop_area", "user", "created_at")
    list_filter = ("farm", "created_at")
    search_fields = ("name",)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "plan", "crop_area", "region", "user", "created_at")
    list_filter = ("region", "farm", "created_at")
    search_fields = ("name",)


@admin.register(Massive)
class MassiveAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "plan", "crop_area", "district", "user", "created_at")
    list_filter = ("district", "farm", "created_at")
    search_fields = ("name",)


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "crop_area", "massive", "user", "created_at")
    list_filter = ("massive", "farm", "created_at")
    search_fields = ("name",)


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "location", "INN", "phone_number")
    search_fields = ("full_name", "INN", "phone_number")
