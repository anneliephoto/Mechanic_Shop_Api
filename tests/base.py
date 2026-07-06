import os
import tempfile
import unittest

from application import create_app
from application.extensions import db
from application.models import Customer, Inventory, Mechanic, ServiceTicket
from application.utils.util import encode_token


class BaseAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db_fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(db_fd)
        cls.db_path = db_path
        cls.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            }
        )
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.engine.dispose()

        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

    def setUp(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

            self.customer = Customer(
                name="Jamie Rivera",
                email="jamie@example.com",
                phone="555-123-4567",
                password="password123",
            )
            self.other_customer = Customer(
                name="Morgan Lee",
                email="morgan@example.com",
                phone="555-987-6543",
                password="password456",
            )
            self.mechanic_one = Mechanic(
                name="Alex Torres",
                email="alex@garage.com",
                phone="555-111-2222",
                salary=42.5,
            )
            self.mechanic_two = Mechanic(
                name="Taylor Reed",
                email="taylor@garage.com",
                phone="555-333-4444",
                salary=48.0,
            )
            self.part_one = Inventory(name="Brake pads", price=89.99)
            self.part_two = Inventory(name="Oil filter", price=14.5)

            db.session.add_all(
                [
                    self.customer,
                    self.other_customer,
                    self.mechanic_one,
                    self.mechanic_two,
                    self.part_one,
                    self.part_two,
                ]
            )
            db.session.commit()

            self.ticket_one = ServiceTicket(
                VIN="1HGCM82633A004352",
                service_date="2026-07-05",
                service_desc="Brake replacement",
                customer_id=self.customer.id,
            )
            self.ticket_two = ServiceTicket(
                VIN="2T1BR32E54C123456",
                service_date="2026-07-06",
                service_desc="Oil change",
                customer_id=self.other_customer.id,
            )
            db.session.add_all([self.ticket_one, self.ticket_two])
            db.session.commit()

            self.ticket_one.mechanics.append(self.mechanic_one)
            self.ticket_one.parts.append(self.part_one)
            self.ticket_two.mechanics.append(self.mechanic_two)
            self.ticket_two.parts.append(self.part_two)
            db.session.commit()

            self.customer_id = self.customer.id
            self.customer_email = self.customer.email
            self.customer_password = self.customer.password
            self.other_customer_id = self.other_customer.id
            self.other_customer_email = self.other_customer.email
            self.mechanic_one_id = self.mechanic_one.id
            self.mechanic_two_id = self.mechanic_two.id
            self.part_one_id = self.part_one.id
            self.part_two_id = self.part_two.id
            self.ticket_one_id = self.ticket_one.id
            self.ticket_two_id = self.ticket_two.id

        self.customer_token = encode_token(self.customer_id)
        self.other_customer_token = encode_token(self.other_customer_id)

    def auth_headers(self, token=None):
        return {"Authorization": f"Bearer {token or self.customer_token}"}
