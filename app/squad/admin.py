from django.contrib import admin, messages
from django.contrib.admin import StackedInline
from django.utils.html import format_html

from app.squad.models import (
    Squad, SquadDailyPicking, Worker, WorkerDailyPicking,
    Territory, Scalesman, CottonPicker, CarDailyPicking,
    Shtab, PickingType, SquadNumber, PQQM, SquadExcelUpload
)
from .utils import import_squad_from_excel


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
    list_display = ("squad_number", "user", "neighborhood", "workers_count")
    search_fields = ("squad_number__number", "user__full_name")
    list_filter = ("neighborhood",)
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
    search_fields = ("squad_number__number", "farm__full_name", "massive__name")


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
    list_display = ("pqqm", "farm", "squad_number", "weight_checked", "tech_number", "created_at")


# ========================= Excel Upload Admin =========================

@admin.register(SquadExcelUpload)
class SquadExcelUploadAdmin(admin.ModelAdmin):
    list_display = ("file", "uploaded_at", "import_result")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            result = import_squad_from_excel(obj.file.path)
            messages.success(
                request,
                f"✅ Import tugadi! {result['created']} yangi squad, {result['updated']} yangilangan, "
                f"{result['skipped']} o'tkazib yuborildi."
            )
        except Exception as e:
            messages.error(request, f"❌ Importda xatolik: {str(e)}")

    def import_result(self, obj):
        return format_html("<span style='color: green;'>✔️ So‘nggi yuklash muvaffaqiyatli</span>")

    import_result.short_description = "Import natijasi"
