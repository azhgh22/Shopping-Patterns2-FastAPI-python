from unittest.mock import ANY

import pytest
from starlette.testclient import TestClient

from playground.core.product import Product, ProductService
from playground.core.receipt import (
    AddProductInput,
    ProductInReceipt,
    Receipt,
    ReceiptService,
    RemoveResults,
)
from playground.infra.Memory.InMemoryModules.product_in_memory_repo import (
    ProductInMemoryRepository,
)
from playground.infra.Memory.InMemoryModules.receipt_in_memory_repo import (
    ReceiptInMemoryRepository,
)
from playground.runner.setup import MemoryType, setup


class TestReceipts:
    @pytest.fixture
    def http(self) -> TestClient:
        return TestClient(setup(MemoryType.IN_MEMORY))

    def test_service_should_persist_receipt(self) -> None:
        receipt_list: list[Receipt] = []
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        rec = service.create()
        assert rec == receipt_list[0]

    def test_service_should_get_none_as_receipt(self) -> None:
        service = ReceiptService(ReceiptInMemoryRepository())
        assert service.get_receipt("1") is None

    def test_service_should_get_receipt_by_id(self) -> None:
        receipt_list = [Receipt("1", "open", [], 0)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        assert receipt_list[0] == service.get_receipt("1")

    def test_service_should_return_none_while_adding_non_existing_product(self) -> None:
        receipt_list = [Receipt("1", "open", [], 0)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        assert (
            service.add_product(
                AddProductInput("1", 2, "1"),
                ProductService(ProductInMemoryRepository()),
            )
            is None
        )

    def test_service_should_return_none_while_adding_to_non_existing_receipt(
        self,
    ) -> None:
        service = ReceiptService(ReceiptInMemoryRepository())
        product_list = [Product("1", "1", "1", "1", 1)]
        assert (
            service.add_product(
                AddProductInput("1", 2, "1"),
                ProductService(ProductInMemoryRepository(product_list)),
            )
            is None
        )

    def test_service_should_add_product_to_receipt(self) -> None:
        product_list = [Product("1", "1", "apple", "23234", 10)]
        receipt_list = [Receipt("1", "open", [], 0)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        service.add_product(
            AddProductInput("1", 3, "1"),
            ProductService(ProductInMemoryRepository(product_list)),
        )
        assert receipt_list[0].total == 30
        assert len(receipt_list[0].products) == 1

    def test_should_just_increase_quantity_while_adding_already_added_one(self) -> None:
        prod_list = [Product("1", "2", "3", "4", 30)]
        receipt_list = [Receipt("1", "open", [ProductInReceipt(prod_list[0], 1)], 30)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        service.add_product(
            AddProductInput("1", 2, "1"),
            ProductService(ProductInMemoryRepository(prod_list)),
        )
        rec = service.get_receipt("1")
        assert rec is not None
        assert len(rec.products) == 1
        assert rec.total == 90

    def test_service_should_return_false_while_closing_non_existing_receipt(
        self,
    ) -> None:
        service = ReceiptService(ReceiptInMemoryRepository())
        assert not service.close_receipt("1", "closed")

    def test_service_should_close_receipt(self) -> None:
        receipt_list = [Receipt("1", "open", [], 0)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        assert service.close_receipt("1", "closed")
        assert receipt_list[0].status == "closed"

    def test_service_should_not_add_product_as_receipt_is_closed(self) -> None:
        product_list = [Product("1", "1", "apple", "23234", 10)]
        receipt_list = [Receipt("1", "closed", [], 0)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        assert (
            service.add_product(
                AddProductInput("1", 3, "1"),
                ProductService(ProductInMemoryRepository(product_list)),
            )
            is None
        )

    def test_service_should_not_delete_non_existing_receipt(self) -> None:
        service = ReceiptService(ReceiptInMemoryRepository())
        assert RemoveResults.RECEIPT_NOT_FOUND == service.delete_receipt("1")

    def test_service_should_not_delete_closed_receipt(self) -> None:
        receipt_list = [Receipt("1", "closed", [], 0)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        assert RemoveResults.RECEIPT_CLOSED == service.delete_receipt("1")

    def test_service_should_delete_receipt(self) -> None:
        receipt_list = [Receipt("1", "open", [], 0)]
        service = ReceiptService(ReceiptInMemoryRepository(receipt_list))
        assert RemoveResults.RECEIPT_REMOVED == service.delete_receipt("1")
        assert len(receipt_list) == 0

    ############
    def test_should_create_new_receipt(self, http: TestClient) -> None:
        response = http.post("/receipts")
        assert response.status_code == 201
        assert response.json() == {
            "id": ANY,
            "status": "open",
            "products": [],
            "total": 0,
        }

    def test_should_return_404_error(self, http: TestClient) -> None:
        rec_id = "333"
        response = http.get(f"/receipts/{rec_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Receipt with id<{rec_id}> does not exist."

    def test_should_persists_receipt(self, http: TestClient) -> None:
        rec_id = http.post("/receipts").json()["id"]
        response = http.get(f"/receipts/{rec_id}")
        assert response.status_code == 200
        assert response.json()["id"] == rec_id

    def test_should_add_product_to_receipt(self, http: TestClient) -> None:
        prod = {"unit_id": "1", "name": "Apple", "barcode": "1234567890", "price": 10}
        receipt_id = http.post("/receipts").json()["id"]
        product_id = http.post("/products", json=prod).json()["id"]
        response = http.post(
            f"/receipts/{receipt_id}/products",
            json={"id": product_id, "quantity": 3},
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": ANY,
            "status": "open",
            "products": [{"id": product_id, "quantity": 3, "price": 10, "total": 30}],
            "total": 30,
        }

    def test_should_close_receipt(self, http: TestClient) -> None:
        receipt_id = http.post("/receipts").json()["id"]
        response = http.patch(f"/receipts/{receipt_id}", json={"status": "closed"})
        assert response.status_code == 200
        receipt = http.get(f"/receipts/{receipt_id}")
        assert receipt.status_code == 200
        assert receipt.json()["status"] == "closed"

    def test_should_delete_receipt(self, http: TestClient) -> None:
        receipt_id = http.post("/receipts").json()["id"]
        assert http.get(f"/receipts/{receipt_id}").status_code == 200
        response = http.delete(f"/receipts/{receipt_id}")
        assert response.status_code == 200
        assert http.get(f"/receipts/{receipt_id}").status_code == 404
