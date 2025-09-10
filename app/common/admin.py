from django.contrib import admin

from django.contrib import admin
from .models import FarmExcelUpload
from .utils import import_farm_from_excel

@admin.register(FarmExcelUpload)
class FarmExcelUploadAdmin(admin.ModelAdmin):
    list_display = ("file", "uploaded_at")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Excel fayldan Farm ma’lumotlarini bazaga qo‘shish
        import_farm_from_excel(obj.file.path)
