from django.core.management.base import BaseCommand
from maintenance.models import Building, Machine, Component, Battery, BatteryReplacementRecord
import csv
import os

EXPORT_DIR = "exported_data"

def import_from_csv(model, filename, fieldnames):
    objs = []
    with open(os.path.join(EXPORT_DIR, filename), newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert fields to correct types if needed
            obj = model(**{field: row[field] for field in fieldnames})
            objs.append(obj)
    model.objects.bulk_create(objs)
    return objs

class Command(BaseCommand):
    help = 'Seeds the database with data from exported CSV files'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        BatteryReplacementRecord.objects.all().delete()
        Battery.objects.all().delete()
        Component.objects.all().delete()
        Machine.objects.all().delete()
        Building.objects.all().delete()

        self.stdout.write('Importing data from CSVs...')

        # Import order: Building -> Machine -> Component -> Battery -> BatteryReplacementRecord
        import_from_csv(Building, "buildings.csv", ["id", "name"])
        import_from_csv(Machine, "machines.csv", ["id", "building_id", "model", "machine_id"])
        import_from_csv(Component, "components.csv", ["id", "machine_id", "name", "model_number", "oem"])
        import_from_csv(Battery, "batteries.csv", [
            "id", "component_id", "oem_part_number", "oem", "replacement_interval_type", "replacement_interval_months"
        ])
        import_from_csv(BatteryReplacementRecord, "battery_replacement_records.csv", [
            "id", "battery_id", "replacement_date"
        ])

        self.stdout.write(self.style.SUCCESS('✅ Database import complete.'))
