import pytest
from starlette.testclient import TestClient

from playground.core.receipt import Receipt
from playground.core.sales import SalesService
from playground.infra.Memory.InMemoryModules.receipt_in_memory_repo import (
    ReceiptInMemoryRepository,
)
from playground.runner.setup import MemoryType, setup


class TestSales:
    @pytest.fixture
    def http(self) -> TestClient:
        return TestClient(setup(MemoryType.IN_MEMORY))

    def test_service_should_return_all_sales(self) -> None:
        receipts_list = [Receipt("1", "2", [], 30), Receipt("2", "2", [], 40)]
        service = SalesService(ReceiptInMemoryRepository(receipts_list))
        response = service.get_sales()
        assert response == {"n_receipts": 2, "revenue": 70}

    def test_should_return_all_sales(self, http: TestClient) -> None:
        receipt_id = http.post("/receipts").json()["id"]
        prod = {"unit_id": "1", "name": "Apple", "barcode": "1234567890", "price": 10}
        product_id = http.post("/products", json=prod).json()["id"]
        http.post(
            f"/receipts/{receipt_id}/products",
            json={"id": product_id, "quantity": 3},
        )
        response = http.get("/sales")
        assert response.status_code == 200
        assert response.json() == {"n_receipts": 1, "revenue": 30}
