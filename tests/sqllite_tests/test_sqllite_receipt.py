import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.product import Product
from playground.core.receipt import ProductInReceipt, Receipt
from playground.infra.Memory.SQLlite.sqllite_product_repo import (
    ProductSqlLiteRepository,
)
from playground.infra.Memory.SQLlite.sqllite_receipt_repo import (
    ReceiptSqlLiteRepository,
)


class TestProductSqlLite:
    @pytest.fixture
    def conn(self) -> Connection:
        file_path = "shop_test.db"
        if os.path.exists(file_path):
            os.remove(file_path)
        return sqlite3.connect(file_path, check_same_thread=False)

    def test_should_create_new_receipt(self, conn: Connection) -> None:
        repo = ReceiptSqlLiteRepository(conn)
        repo.create(Receipt("1", "open", [], 1))
        raw = conn.execute("SELECT * FROM receipts").fetchone()
        assert raw is not None
        assert raw[0] == "1"
        assert raw[1] == "open"
        assert raw[2] == 1

        conn.close()

    def test_should_add_new_product_to_receipt(self, conn: Connection) -> None:
        repo = ReceiptSqlLiteRepository(conn)
        repo.add_product_to_receipt(
            ProductInReceipt(Product("1", "1", "1", "1", 1), 3), "2"
        )

        raw = conn.execute("SELECT * FROM receipt_product_linker").fetchone()

        assert raw is not None
        assert raw[0] == "2"  # check receipt_id
        assert raw[1] == "1"  # check product_id
        assert raw[2] == 3  # check total
        conn.close()

    def test_should_update_receipt_status(self, conn: Connection) -> None:
        repo = ReceiptSqlLiteRepository(conn)
        repo.create(Receipt("1", "open", [], 1))
        assert repo.update_status("1", "closed")
        raw = conn.execute("SELECT status FROM receipts").fetchone()
        assert raw is not None
        assert raw[0] == "closed"
        conn.close()

    def test_should_increase_receipt_total(self, conn: Connection) -> None:
        repo = ReceiptSqlLiteRepository(conn)
        repo.create(Receipt("1", "open", [], 1))
        repo.increase_receipt_total("1", 10)
        row = conn.execute("SELECT total FROM receipts").fetchone()
        assert row[0] == 11
        conn.close()

    def test_checks_whether_or_not_receipt_contains_product(
        self, conn: Connection
    ) -> None:
        repo = ReceiptSqlLiteRepository(conn)
        repo.add_product_to_receipt(
            ProductInReceipt(Product("1", "1", "1", "1", 1), 2), "2"
        )

        assert repo.receipt_has_product("1", "2")
        conn.close()

    def test_should_return_sales_info(self, conn: Connection) -> None:
        repo = ReceiptSqlLiteRepository(conn)
        repo.create(Receipt("1", "open", [], 1))
        repo.create(Receipt("2", "open", [], 11))
        sales = repo.get_sales_info()
        assert sales.n_receipts == 2
        assert sales.total == 12

        conn.close()

    def test_should_remove_receipt(self, conn: Connection) -> None:
        repo = ReceiptSqlLiteRepository(conn)
        repo.create(Receipt("1", "open", [], 1))
        repo.add_product_to_receipt(
            ProductInReceipt(Product("1", "1", "1", "1", 1), 3), "1"
        )

        repo.remove("1")
        assert conn.execute("SELECT count(*) FROM receipts").fetchone()[0] == 0
        assert (
            conn.execute("SELECT count(*) FROM receipt_product_linker").fetchone()[0]
            == 0
        )
        conn.close()

    def test_should_get_receipt(self, conn: Connection) -> None:
        prod1 = Product("1", "1", "1", "1", 1)
        prod2 = Product("2", "2", "2", "2", 2)

        prod_repo = ProductSqlLiteRepository(conn)
        prod_repo.create(prod1)
        prod_repo.create(prod2)

        repo = ReceiptSqlLiteRepository(conn)

        repo.create(Receipt("1", "open", [], 0))
        repo.add_product_to_receipt(ProductInReceipt(prod1, 1), "1")
        repo.add_product_to_receipt(ProductInReceipt(prod2, 2), "1")
        repo.increase_receipt_total("1", 5)
        receipt = repo.get_receipt("1")
        assert receipt is not None
        assert receipt.id == "1"
        assert receipt.total == 5
        assert len(receipt.products) == 2

        conn.close()
