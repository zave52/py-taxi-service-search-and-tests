from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class PublicTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        Driver.objects.create(
            username="test",
            password="test12345"
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

    def test_login_required_driver(self) -> None:
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:driver-detail", args=[1]))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:driver-delete", args=[1]))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:driver-update", args=[1]))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car(self) -> None:
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:car-detail", args=[1]))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:car-delete", args=[1]))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:car-update", args=[1]))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer(self) -> None:
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:manufacturer-update", args=[1]))
        self.assertNotEqual(res.status_code, 200)
        res = self.client.get(reverse("taxi:manufacturer-delete", args=[1]))
        self.assertNotEqual(res.status_code, 200)


class PrivateTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Driver.objects.create(
            username="test1",
            password="test12345",
            license_number="test1"
        )
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test country1"
        )
        Manufacturer.objects.create(
            name="test2",
            country="test country2"
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

    def setUp(self) -> None:
        user = Driver.objects.create_superuser(
            username="test2",
            password="test12345",
            license_number="test2"
        )
        self.client.force_login(user)

    def test_retrieve_manufacturers(self) -> None:
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self) -> None:
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self) -> None:
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer1
        )
        Car.objects.create(
            model="Mustang",
            manufacturer=manufacturer2
        )
        Driver.objects.create(
            username="driver1",
            password="pass1",
            license_number="test1"
        )
        Driver.objects.create(
            username="driver2",
            password="pass2",
            license_number="test2"
        )

    def setUp(self) -> None:
        user = Driver.objects.create_superuser(
            username="test1",
            password="test12345",
            license_number="test3"
        )
        self.client.force_login(user)

    def test_search_manufacturer_by_name(self) -> None:
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_car_by_model(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Corolla"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Mustang")

    def test_search_driver_by_username(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")
