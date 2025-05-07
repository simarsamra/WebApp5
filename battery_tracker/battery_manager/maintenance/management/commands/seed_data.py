from django.core.management.base import BaseCommand
from maintenance.models import Machine, Component, BatteryModel, BatteryReplacementRecord, ComponentModel
from django.contrib.auth.models import User
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds dummy data for testing'

    def handle(self, *args, **options):
        # Create a superuser if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password('password123')  # Set a default password
            user.save()
            self.stdout.write(self.style.SUCCESS("✅ Superuser 'testuser' created with password 'password123'."))

        # Create dummy battery models
        battery_models = [
            BatteryModel.objects.get_or_create(
                name="BR-AGCF2W", oem="Panasonic", oem_part_number="BR-AGCF2W"
            )[0],
            BatteryModel.objects.get_or_create(
                name="BR-AGCF3X", oem="Samsung", oem_part_number="BR-AGCF3X"
            )[0],
            BatteryModel.objects.get_or_create(
                name="BR-AGCF4Y", oem="LG", oem_part_number="BR-AGCF4Y"
            )[0],
            BatteryModel.objects.get_or_create(
                name="BR-AGCF5Z", oem="Sony", oem_part_number="BR-AGCF5Z"
            )[0],
        ]

        # Create dummy component models
        component_models = [
            ComponentModel.objects.get_or_create(
                name="Drive", description="Drive components used in the machines"
            )[0],
            ComponentModel.objects.get_or_create(
                name="Motor", description="Motors used in the machines"
            )[0],
            ComponentModel.objects.get_or_create(
                name="Sensor", description="Sensor components used in the machines"
            )[0],
        ]

        # Create dummy machines and their components
        for i in range(8):
            machine, _ = Machine.objects.get_or_create(
                building=f"Building {i+1}",
                machine_id=1000 + i,
                model=f"Model {i+1}",
                year_of_manufacture=2020 + i,
            )

            # Create components for each machine
            for j in range(3):  # Each machine has 3 components
                component, _ = Component.objects.get_or_create(
                    machine=machine,
                    component_model=component_models[j % len(component_models)],
                    battery_model=battery_models[j % len(battery_models)],
                    procedure_document_link=f"/documents/procedure_{i+1}_{j+1}.pdf",
                )

                # Create battery replacement records for each component
                BatteryReplacementRecord.objects.get_or_create(
                    component=component,
                    battery_model=component.battery_model,
                    replacement_interval="365 Days",
                    last_replaced=date.today() - timedelta(days=30),
                    due_date=date.today() + timedelta(days=335),
                    replaced_by=user,
                )

        self.stdout.write(self.style.SUCCESS("✅ Dummy data for 8 machines created successfully."))
