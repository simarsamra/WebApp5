from django.contrib import admin
from .models import Machine, Component, BatteryReplacementRecord, BatteryModel, ComponentModel


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1  # Number of empty forms to display
    fields = ('component_model',)
    show_change_link = True


class BatteryReplacementRecordInline(admin.TabularInline):
    model = BatteryReplacementRecord
    extra = 1
    fields = ('due_date', 'last_replaced')
    show_change_link = True


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('building', 'machine_id', 'model')
    search_fields = ('machine_id', 'model', 'building')
    list_filter = ('building',)
    inlines = [ComponentInline]  # Add inline editing for components


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('component_model', 'machine')
    search_fields = ('component_model', 'machine__model', 'machine__building')
    list_filter = ('machine__building',)
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
    list_display = ('component', 'due_date', 'last_replaced')
    list_filter = ('due_date', 'last_replaced')
    search_fields = ('component__component_model', 'component__machine__model')
    date_hierarchy = 'last_replaced'  # Add a date hierarchy for better navigation
