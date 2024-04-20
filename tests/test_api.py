# tests/test_api.py
import json
import unittest
from flask_testing import TestCase
from src.online_store.models.models import Product
from src.online_store.app import app, db


class TestBase(TestCase):
    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()
            # Создаем продукт для тестирования удаления, обновления, получения
            product = Product(
                name="Test Product",
                description="A test item",
                price=19.99,
                quantity=100,
            )
            db.session.add(product)
            db.session.commit()
            self.product_id = product.id  # Сохраняем ID для использования в тестах

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class TestViews(TestBase):
    def test_add_product(self):
        response = self.client.post(
            "/products",
            data=json.dumps(
                {
                    "name": "New Test Product",
                    "description": "A new test item",
                    "price": 24.99,
                    "quantity": 50,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 308)

    def test_get_all_products(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 308)

    def test_get_product(self):
        response = self.client.get(f"/products/{self.product_id}")
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        response = self.client.put(
            f"/products/{self.product_id}",
            data=json.dumps(
                {
                    "name": "Updated Test Product",
                    "description": "An updated test item",
                    "price": 29.99,
                    "quantity": 75,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        response = self.client.delete(f"/products/{self.product_id}")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
