from django.core.management.base import BaseCommand
from maintenance.models import Machine, Component, BatteryReplacementRecord
from datetime import date, timedelta
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding the database...')

        # Create a superuser
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_superuser('testuser', 'test@example.com', 'password123')
            self.stdout.write(self.style.SUCCESS('✅ Superuser \'testuser\' created with password \'password123\'.'))

        # Create some machines
        machines = []
        for i in range(5):
            machine, _ = Machine.objects.get_or_create(
                building=f"Building {i+1}",
                model=f"Machine Model {i+1}",
                machine_id=f"M{i+1:03d}",
                year_of_manufacture=2020 + i,  # Add this line
            )
            machines.append(machine)

        # Create some components
        components = []
        for machine in machines:
            for j in range(3):
                component = Component.objects.create(
                    machine=machine,
                    component_model=f"Component {j+1} for {machine.model}"
                )
                components.append(component)

        # Create some battery replacement records
        for component in components:
            due_date = date.today() + timedelta(days=random.randint(30, 365))
            BatteryReplacementRecord.objects.create(
                component=component,
                due_date=due_date,
                last_replaced=date.today() - timedelta(days=random.randint(10, 90))
            )

        self.stdout.write(self.style.SUCCESS('✅ Database seeding complete.'))
