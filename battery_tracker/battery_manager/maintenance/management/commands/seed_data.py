from django.core.management.base import BaseCommand
from maintenance.models import Building, Machine, Component, Battery, BatteryReplacementRecord
from datetime import date, timedelta
import random
from random import choice, randint

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        BatteryReplacementRecord.objects.all().delete()
        Battery.objects.all().delete()
        Component.objects.all().delete()
        Machine.objects.all().delete()
        Building.objects.all().delete()

        self.stdout.write('Seeding the database...')

        # Create buildings
        buildings = []
        for i in range(2):
            building, _ = Building.objects.get_or_create(name=f"Building {i+1}")
            buildings.append(building)

        # Create machines
        machines = []
        for i, building in enumerate(buildings):
            for j in range(3):
                machine, _ = Machine.objects.get_or_create(
                    building=building,
                    model=f"Machine Model {j+1}",
                    machine_id=f"M{i+1}{j+1:02d}"
                )
                machines.append(machine)

        # Create components
        components = []
        for machine in machines:
            for k in range(2):
                component, _ = Component.objects.get_or_create(
                    machine=machine,
                    name=f"Component {k+1} for {machine.model}",
                    model_number=f"CM{k+1:03d}",
                    oem=f"OEM {k+1}"
                )
                components.append(component)

        # Create batteries
        batteries = []
        for component in components:
            for l in range(1):
                interval_type = choice(['months', 'alarm'])
                if interval_type == 'months':
                    interval_months = randint(3, 24)
                else:
                    interval_months = None
                battery, _ = Battery.objects.get_or_create(
                    component=component,
                    oem_part_number=f"BATT-{l+1:03d}",
                    oem=f"Battery OEM {l+1}",
                    replacement_interval_type=interval_type,
                    replacement_interval_months=interval_months
                )
                batteries.append(battery)

        # Create battery replacement records
        for battery in batteries:
            for m in range(2):
                BatteryReplacementRecord.objects.create(
                    battery=battery,
                    replacement_date=date.today() - timedelta(days=random.randint(1, 100))
                )

        self.stdout.write(self.style.SUCCESS('✅ Database seeding complete.'))
