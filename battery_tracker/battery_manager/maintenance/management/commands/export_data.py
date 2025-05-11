from django.core.management.base import BaseCommand
from maintenance.models import Building, Machine, Component, Battery, BatteryReplacementRecord
import csv
import os

EXPORT_DIR = "exported_data"

class Command(BaseCommand):
    help = "Export all maintenance app data to CSV files"

    def handle(self, *args, **options):
        os.makedirs(EXPORT_DIR, exist_ok=True)

        # Export Buildings
        with open(os.path.join(EXPORT_DIR, "buildings.csv"), "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name"])
            for obj in Building.objects.all():
                writer.writerow([obj.id, obj.name])

        # Export Machines
        with open(os.path.join(EXPORT_DIR, "machines.csv"), "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "building_id", "model", "machine_id"])
            for obj in Machine.objects.all():
                writer.writerow([obj.id, obj.building_id, obj.model, obj.machine_id])

        # Export Components
        with open(os.path.join(EXPORT_DIR, "components.csv"), "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "machine_id", "name", "model_number", "oem"])
            for obj in Component.objects.all():
                writer.writerow([obj.id, obj.machine_id, obj.name, obj.model_number, obj.oem])

        # Export Batteries
        with open(os.path.join(EXPORT_DIR, "batteries.csv"), "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "component_id", "oem_part_number", "oem",
                "replacement_interval_type", "replacement_interval_months"
            ])
            for obj in Battery.objects.all():
                writer.writerow([
                    obj.id, obj.component_id, obj.oem_part_number, obj.oem,
                    obj.replacement_interval_type, obj.replacement_interval_months
                ])

        # Export BatteryReplacementRecords
        with open(os.path.join(EXPORT_DIR, "battery_replacement_records.csv"), "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "battery_id", "replacement_date"])
            for obj in BatteryReplacementRecord.objects.all():
                writer.writerow([obj.id, obj.battery_id, obj.replacement_date])

        self.stdout.write(self.style.SUCCESS("✅ Data exported to 'exported_data/' folder."))