from tests.base import BaseAPITestCase


class TestInventoryAPI(BaseAPITestCase):
    def test_create_part_success(self):
        response = self.client.post(
            "/inventory",
            json={"name": "Air filter", "price": 19.99},
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "Air filter")

    def test_get_parts_returns_list(self):
        response = self.client.get("/inventory")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_get_part_success(self):
        response = self.client.get(f"/inventory/{self.part_one_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Brake pads")

    def test_get_part_not_found_returns_404(self):
        response = self.client.get("/inventory/9999")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    def test_update_part_success(self):
        response = self.client.put(
            f"/inventory/{self.part_two_id}",
            json={"name": "Oil filter updated", "price": 22.5},
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Oil filter updated")

    def test_delete_part_success(self):
        response = self.client.delete(f"/inventory/{self.part_two_id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
