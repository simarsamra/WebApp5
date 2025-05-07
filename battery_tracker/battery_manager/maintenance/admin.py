from django.contrib import admin
from .models import Machine, Component, BatteryModel, BatteryReplacementRecord, ComponentModel


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1  # Number of empty forms to display
    fields = ('component_model', 'battery_model', 'procedure_document_link')
    show_change_link = True


class BatteryReplacementRecordInline(admin.TabularInline):
    model = BatteryReplacementRecord
    extra = 1
    fields = ('battery_model', 'replacement_interval', 'last_replaced', 'due_date', 'replaced_by')
    show_change_link = True


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('building', 'machine_id', 'model', 'year_of_manufacture')
    search_fields = ('machine_id', 'model', 'building')
    list_filter = ('building', 'year_of_manufacture')
    inlines = [ComponentInline]  # Add inline editing for components


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('component_model', 'machine', 'battery_model', 'procedure_document_link')
    search_fields = ('component_model__name', 'machine__model', 'machine__building')
    list_filter = ('machine__building', 'battery_model__name', 'component_model__name')
    inlines = [BatteryReplacementRecordInline]  # Add inline editing for battery replacement records


@admin.register(BatteryModel)
class BatteryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'oem', 'oem_part_number')
    search_fields = ('name', 'oem', 'oem_part_number')
    list_filter = ('oem',)


@admin.register(ComponentModel)
class ComponentModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(BatteryReplacementRecord)
class BatteryReplacementRecordAdmin(admin.ModelAdmin):
    list_display = (
        'component', 'battery_model', 'replacement_interval',
        'last_replaced', 'due_date', 'replaced_by'
    )
    list_filter = ('replacement_interval', 'battery_model', 'last_replaced', 'due_date')
    search_fields = ('component__component_model__name', 'battery_model__name', 'component__machine__model')
    date_hierarchy = 'last_replaced'  # Add a date hierarchy for better navigation
