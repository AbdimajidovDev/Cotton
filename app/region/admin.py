from django.contrib import admin
from .models import Region, District, Massive, Neighborhood, Farm
from .models import FarmExcelUpload
from .utils import import_farm_from_excel


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "plan", "crop_area", "created_at")
    search_fields = ("name",)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "plan", "crop_area", "created_at")
    list_filter = ("region",)
    search_fields = ("name",)


@admin.register(Massive)
class MassiveAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "plan", "crop_area", "created_at")
    list_filter = ("district",)
    search_fields = ("name",)


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ("name", "massive", "crop_area", "created_at")
    list_filter = ("massive",)
    search_fields = ("name",)


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("full_name", "massive_name", "INN", "phone_number", "region", "district", "cotton_area")
    list_filter = ("region", "district", "massive")
    search_fields = ("full_name", "INN", "phone_number")


@admin.register(FarmExcelUpload)
class FarmExcelUploadAdmin(admin.ModelAdmin):
    list_display = ("file", "uploaded_at")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.file:
            try:
                import_farm_from_excel(obj.file.path)
            except Exception as e:
                self.message_user(
                    request,
                    f"Excel fayldan ma’lumot import qilishda xatolik yuz berdi: {e}",
                    level='error'
                )
