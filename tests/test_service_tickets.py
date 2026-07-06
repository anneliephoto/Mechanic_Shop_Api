from tests.base import BaseAPITestCase


class TestServiceTicketsAPI(BaseAPITestCase):
    def test_create_service_ticket_success(self):
        response = self.client.post(
            "/service_tickets",
            json={
                "VIN": "3FAHP0HA6AR123456",
                "service_date": "2026-07-07",
                "service_desc": "Tire rotation",
                "customer_id": self.customer_id,
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["VIN"], "3FAHP0HA6AR123456")

    def test_get_service_tickets_returns_list(self):
        response = self.client.get("/service_tickets")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_assign_mechanic_success(self):
        response = self.client.put(
            f"/service_tickets/{self.ticket_one_id}/assign-mechanic/{self.mechanic_two_id}"
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)

    def test_assign_mechanic_missing_mechanic_returns_404(self):
        response = self.client.put(
            f"/service_tickets/{self.ticket_one_id}/assign-mechanic/9999"
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    def test_remove_mechanic_success(self):
        response = self.client.put(
            f"/service_tickets/{self.ticket_one_id}/remove-mechanic/{self.mechanic_one_id}"
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)

    def test_edit_ticket_mechanics_success(self):
        response = self.client.put(
            f"/service_tickets/{self.ticket_one_id}/edit",
            json={"add_ids": [self.mechanic_two_id], "remove_ids": [self.mechanic_one_id]},
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["added_ids"], [self.mechanic_two_id])
        self.assertEqual(data["removed_ids"], [self.mechanic_one_id])

    def test_add_part_to_ticket_success(self):
        response = self.client.put(
            f"/service_tickets/{self.ticket_one_id}/add-part/{self.part_two_id}"
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
