from unittest.mock import ANY

import pytest
from starlette.testclient import TestClient

from playground.core.product import Product, ProductCreateRequestModel, ProductService
from playground.infra.Memory.InMemoryModules.product_in_memory_repo import (
    ProductInMemoryRepository,
)
from playground.runner.setup import MemoryType, setup


class TestProduct:
    @pytest.fixture
    def http(self) -> TestClient:
        return TestClient(setup(MemoryType.IN_MEMORY))

    def test_should_read_empty_list_of_products(self, http: TestClient) -> None:
        response = http.get("/products")
        assert response.status_code == 200
        assert response.json() == []

    def test_should_return_return_404_error(self, http: TestClient) -> None:
        product_id = 123
        response = http.get(f"/products/{product_id}")
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == f"Product with id<{product_id}> does not exist."
        )

    def test_should_create_new_product(self, http: TestClient) -> None:
        new_product = {
            "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520,
        }
        response = http.post("/products", json=new_product)
        assert response.status_code == 201
        assert response.json() == {"id": ANY, **new_product}

    def test_should_persist_product(self, http: TestClient) -> None:
        new_product = {
            "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520,
        }

        create_res = http.post("/products", json=new_product)
        assert create_res.status_code == 201
        product_id = create_res.json()["id"]

        get_response = http.get(f"/products/{product_id}")
        assert get_response.status_code == 200
        assert get_response.json() == {"id": ANY, **new_product}

    def test_should_return_409_error(self, http: TestClient) -> None:
        new_product = {
            "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520,
        }

        create_res = http.post("/products", json=new_product)
        assert create_res.status_code == 201

        create_res = http.post("/products", json=new_product)
        assert create_res.status_code == 409
        assert (
            create_res.json()["detail"]
            == f"Product with barcode<{new_product["barcode"]}> already exists."
        )

    def test_service_should_return_all_products(self) -> None:
        product_list = [Product("0", "1", "2", "3", 4)]
        response_list = ProductService(
            ProductInMemoryRepository(product_list)
        ).get_all()
        assert len(response_list) == len(product_list)
        assert response_list[0].name == product_list[0].name

    def test_should_return_all_products(self, http: TestClient) -> None:
        new_product = {
            "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520,
        }

        http.post("/products", json=new_product)
        new_product["barcode"] = "2343252322"
        http.post("/products", json=new_product)
        response = http.get("/products")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_should_create_store_products(self) -> None:
        product_list: list[Product] = []
        product_service = ProductService(ProductInMemoryRepository(product_list))
        product_service.create(ProductCreateRequestModel("1", "2", "3", 4))
        assert product_list[0].name == "2"

    def test_should_update_product_price(self) -> None:
        product_list = [Product("0", "1", "2", "3", 4)]
        product_service = ProductService(ProductInMemoryRepository(product_list))
        product_service.update("0", 20)
        assert product_list[0].price == 20

    def test_should_update_existing_product(self, http: TestClient) -> None:
        new_product = {
            "unit_id": "27b4f218-1cc2-4694-b131-ad481dc08901",
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520,
        }
        prod_id = http.post("/products", json=new_product).json()["id"]
        res = http.patch(f"/products/{prod_id}", json={"price": 20})
        assert res.status_code == 200
        res2 = http.get(f"/products/{prod_id}")
        assert res2.status_code == 200
        assert res2.json()["price"] == 20
