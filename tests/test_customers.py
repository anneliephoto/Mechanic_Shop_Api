from application.utils.util import decode_token

from tests.base import BaseAPITestCase


class TestCustomersAPI(BaseAPITestCase):
    def test_login_customer_success(self):
        response = self.client.post(
            "/customers/login",
            json={"email": self.customer_email, "password": self.customer_password},
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", data)
        self.assertEqual(decode_token(data["token"]), self.customer.id)

    def test_create_customer_success(self):
        response = self.client.post(
            "/customers",
            json={
                "name": "Casey Green",
                "email": "casey@example.com",
                "phone": "555-222-3333",
                "password": "secret123",
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["email"], "casey@example.com")

    def test_create_customer_duplicate_email_returns_400(self):
        response = self.client.post(
            "/customers",
            json={
                "name": "Duplicate User",
                "email": self.customer_email,
                "phone": "555-444-5555",
                "password": "secret123",
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

    def test_get_customers_returns_paginated_list(self):
        response = self.client.get("/customers?limit=1&offset=0")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", data)
        self.assertIn("pagination", data)
        self.assertEqual(data["pagination"]["limit"], 1)

    def test_get_my_tickets_success(self):
        response = self.client.get("/customers/my-tickets", headers=self.auth_headers())
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_customer_forbidden_returns_403(self):
        response = self.client.get(
            f"/customers/{self.customer_id}",
            headers=self.auth_headers(self.other_customer_token),
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 403)
        self.assertIn("error", data)

    def test_update_customer_success(self):
        response = self.client.put(
            f"/customers/{self.customer_id}",
            headers=self.auth_headers(),
            json={
                "name": "Jamie Rivera Updated",
                "email": "jamie.updated@example.com",
                "phone": "555-777-8888",
                "password": "password123",
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "Jamie Rivera Updated")

    def test_delete_customer_success(self):
        response = self.client.delete(
            f"/customers/{self.customer_id}",
            headers=self.auth_headers(),
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
