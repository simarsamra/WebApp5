from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Building, Machine, Component, Battery, BatteryReplacementRecord

@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin):
    list_display = ('model', 'machine_id', 'building')
    search_fields = ('model', 'machine_id', 'building__name')
    list_filter = ('building',)

@admin.register(Component)
class ComponentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'model_number', 'oem', 'machine')
    search_fields = ('name', 'model_number', 'oem', 'machine__machine_id')
    list_filter = ('machine__building', 'machine')

@admin.register(Battery)
class BatteryAdmin(ImportExportModelAdmin):
    list_display = ('oem', 'oem_part_number', 'component')
    search_fields = ('oem', 'oem_part_number', 'component__name')
    list_filter = ('component__machine__building',)

@admin.register(BatteryReplacementRecord)
class BatteryReplacementRecordAdmin(ImportExportModelAdmin):
    list_display = ('battery', 'replacement_date', 'logged_at')
    search_fields = ('battery__oem', 'battery__oem_part_number', 'battery__component__name')
    list_filter = ('replacement_date', 'battery__component__machine__building')
