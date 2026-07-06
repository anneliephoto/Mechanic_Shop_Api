from tests.base import BaseAPITestCase


class TestMechanicsAPI(BaseAPITestCase):
    def test_create_mechanic_success(self):
        response = self.client.post(
            "/mechanics",
            json={
                "name": "Jordan Blake",
                "email": "jordan@example.com",
                "phone": "555-888-9999",
                "salary": 55.5,
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["email"], "jordan@example.com")

    def test_create_mechanic_missing_field_returns_400(self):
        response = self.client.post(
            "/mechanics",
            json={
                "name": "Missing Salary",
                "email": "missing@example.com",
                "phone": "555-000-1111",
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("salary", data)

    def test_get_mechanics_returns_list(self):
        response = self.client.get("/mechanics")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_update_mechanic_success(self):
        response = self.client.put(
            f"/mechanics/{self.mechanic_one_id}",
            json={
                "name": "Alex Torres Updated",
                "email": "alex.updated@garage.com",
                "phone": "555-111-0000",
                "salary": 60.0,
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Alex Torres Updated")

    def test_delete_mechanic_success(self):
        response = self.client.delete(f"/mechanics/{self.mechanic_two_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)

    def test_get_most_active_mechanics_returns_ranked_list(self):
        response = self.client.get("/mechanics/most-active")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertIn("ticket_count", data[0])
