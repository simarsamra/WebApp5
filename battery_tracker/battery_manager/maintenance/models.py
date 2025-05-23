from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Machine(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="machines")
    model = models.CharField(max_length=100)
    machine_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.model} ({self.machine_id}) in {self.building.name}"

class Component(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="components")
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    oem = models.CharField(max_length=100)
    procedure_document = models.FileField(
        upload_to='procedure_documents/', blank=True, null=True,
        help_text="Upload a document for the replacement procedure (optional)."
    )

    def __str__(self):
        return f"{self.name} ({self.model_number}) on {self.machine}"

class Battery(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="batteries")
    oem_part_number = models.CharField(max_length=100)
    oem = models.CharField(max_length=100)
    REPLACEMENT_TYPE_CHOICES = [
        ('months', 'Months'),
        ('alarm', 'On Alarm'),
    ]
    replacement_interval_type = models.CharField(
        max_length=10,
        choices=REPLACEMENT_TYPE_CHOICES,
        default='months'
    )
    replacement_interval_months = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Number of months between replacements (if interval type is months)"
    )

    def __str__(self):
        return (
            f"{self.oem} ({self.oem_part_number}) for {self.component}"
        )

class BatteryReplacementRecord(models.Model):
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name="replacement_records")
    replacement_date = models.DateField()
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replacement for {self.battery} on {self.replacement_date}"
