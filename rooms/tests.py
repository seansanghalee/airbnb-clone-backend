from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESCRIPTION = "Test Description"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code not 200",
        )

        self.assertIsInstance(data, list, "Data not list.")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESCRIPTION)

    def test_create_amenity(self):
        name = "New Amenity"
        description = "New Description"
        data = {
            "name": name,
            "description": description,
        }
        response = self.client.post(
            self.URL,
            data=data,
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Status code not 200",
        )
        self.assertEqual(
            data["name"],
            name,
        )
        self.assertEqual(
            data["description"],
            description,
        )


class TestAmenity(APITestCase):
    NAME = "Test Amenity"
    DESCRIPTION = "Test Description"
    URL = "/api/v1/rooms/amenities/1"
    BAD_URL = "/api/v1/rooms/amenities/2"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
        )

    def test_get_amenity(self):
        response = self.client.get(self.BAD_URL)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESCRIPTION)

    def test_put_amenity(self):
        pass

    def test_delete_amenity(self):
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403)

        self.client.login(
            username="test",
            password="123",
        )
        self.client.force_login(
            self.user,
        )  # force_login only requires a user

        response = self.client.post("/api/v1/rooms/")
        print(response)
