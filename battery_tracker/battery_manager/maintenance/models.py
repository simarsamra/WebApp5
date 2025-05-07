from django.db import models
from django.contrib.auth.models import User

class Machine(models.Model):
    building = models.CharField(max_length=100)
    machine_id = models.IntegerField()
    model = models.CharField(max_length=100)
    year_of_manufacture = models.IntegerField()

    def __str__(self):
        return f"{self.model} ({self.machine_id}) - {self.building}"

class BatteryModel(models.Model):
    name = models.CharField(max_length=100)
    oem = models.CharField(max_length=100)
    oem_part_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.oem_part_number})"

class ComponentModel(models.Model):  # New model for component type
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Component(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='components')
    component_model = models.ForeignKey(ComponentModel, on_delete=models.CASCADE)  # Replacing controller_hmi_drive
    battery_model = models.ForeignKey(BatteryModel, on_delete=models.CASCADE, null=True, blank=True)
    procedure_document_link = models.FileField(
        upload_to='procedures/', null=True, blank=True,
        help_text="PDF or document describing battery replacement for this component"
    )

    def __str__(self):
        return f"{self.component_model} ({self.machine})"

class BatteryReplacementRecord(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='battery_replacements')
    battery_model = models.ForeignKey(BatteryModel, on_delete=models.PROTECT)
    replacement_interval = models.CharField(max_length=100)
    last_replaced = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    replaced_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.battery_model.name} on {self.component.machine} - {self.last_replaced}"
