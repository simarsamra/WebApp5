from django.db import models
from django.contrib.auth.models import User

class Machine(models.Model):
    building = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    machine_id = models.CharField(max_length=50)
    year_of_manufacture = models.IntegerField(null=True, blank=True)  # Add this line

    def __str__(self):
        return f"{self.model} ({self.machine_id})"

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
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    component_model = models.CharField(max_length=100)

    def __str__(self):
        return self.component_model

class BatteryReplacementRecord(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    due_date = models.DateField()
    last_replaced = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Replacement for {self.component} due on {self.due_date}"
