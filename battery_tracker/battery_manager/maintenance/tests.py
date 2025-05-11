from django.test import TestCase
from django.urls import reverse
from .models import Building, Machine, Component, Battery
from django.contrib.auth.models import User

class BasicViewTests(TestCase):
    def test_home_page_loads(self):
        # This test checks if the home page loads successfully (returns HTTP 200)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_login(self):
        # This test checks if the admin login page loads
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)

class BuildingModelTest(TestCase):
    def test_create_building(self):
        # This test checks if a Building object can be created and its string representation is correct
        b = Building.objects.create(name="Test Building")
        self.assertEqual(str(b), "Test Building")
        self.assertEqual(Building.objects.count(), 1)

class MachineModelTest(TestCase):
    def setUp(self):
        # Set up a Building instance for use in Machine tests
        self.building = Building.objects.create(name="Main Building")

    def test_create_machine(self):
        # This test checks if a Machine object can be created and its string representation is correct
        m = Machine.objects.create(
            building=self.building,
            model="Model X",
            machine_id="MX001"
        )
        self.assertEqual(str(m), "Model X (MX001)")
        self.assertEqual(Machine.objects.count(), 1)

class ComponentModelTest(TestCase):
    def setUp(self):
        # Set up Building and Machine instances for use in Component tests
        self.building = Building.objects.create(name="Main Building")
        self.machine = Machine.objects.create(
            building=self.building,
            model="Model X",
            machine_id="MX001"
        )

    def test_create_component(self):
        # This test checks if a Component object can be created and its string representation is correct
        c = Component.objects.create(
            machine=self.machine,
            name="Battery Compartment",
            model_number="BC-100",
            oem="OEM Inc"
        )
        self.assertEqual(str(c), "Battery Compartment (BC-100)")
        self.assertEqual(Component.objects.count(), 1)

class BatteryModelTest(TestCase):
    def setUp(self):
        # Set up Building, Machine, and Component instances for use in Battery tests
        self.building = Building.objects.create(name="Main Building")
        self.machine = Machine.objects.create(
            building=self.building,
            model="Model X",
            machine_id="MX001"
        )
        self.component = Component.objects.create(
            machine=self.machine,
            name="Battery Compartment",
            model_number="BC-100",
            oem="OEM Inc"
        )

    def test_create_battery(self):
        # This test checks if a Battery object can be created
        b = Battery.objects.create(
            component=self.component,
            oem_part_number="BAT-123",
            oem="OEM Battery"
        )
        self.assertEqual(Battery.objects.count(), 1)

class UserModelTest(TestCase):
    def test_create_user(self):
        # This test checks if a User object can be created
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(user.check_password('testpass'))
