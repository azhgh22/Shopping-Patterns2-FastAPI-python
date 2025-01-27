import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.product import Product
from playground.infra.Memory.SQLlite.sqllite_product_repo import (
    ProductSqlLiteRepository,
)


def check_equality(prod1: Product | None, prod2: Product) -> None:
    assert prod1 is not None
    assert prod1.id == prod2.id
    assert prod1.unit_id == prod2.unit_id
    assert prod1.name == prod2.name
    assert prod1.barcode == prod2.barcode
    assert prod1.price == prod2.price


class TestProductSqlLite:
    @pytest.fixture
    def conn(self) -> Connection:
        file_path = "shop_test.db"
        if os.path.exists(file_path):
            os.remove(file_path)
        return sqlite3.connect(file_path, check_same_thread=False)

    def test_should_create_product(self, conn: Connection) -> None:
        repo = ProductSqlLiteRepository(conn)
        prod = Product("1", "1", "1", "11", 520)
        repo.create(prod)

        raw = conn.execute(
            """
            select * from products where id = ?
        """,
            prod.id,
        ).fetchone()

        check_equality(Product(raw[0], raw[1], raw[2], raw[3], raw[4]), prod)
        conn.close()

    def test_should_get_product_with_id(self, conn: Connection) -> None:
        repo = ProductSqlLiteRepository(conn)
        repo.create(Product("1", "1", "1", "11", 520))
        check_equality(repo.get("1"), Product("1", "1", "1", "11", 520))
        conn.close()

    def test_should_get_product_with_barcode(self, conn: Connection) -> None:
        repo = ProductSqlLiteRepository(conn)
        repo.create(Product("1", "1", "1", "11", 520))

        check_equality(repo.get_with_barcode("11"), Product("1", "1", "1", "11", 520))
        conn.close()

    def test_should_get_all_products(self, conn: Connection) -> None:
        product_list = [Product("1", "1", "1", "1", 1), Product("2", "2", "2", "2", 2)]
        repo = ProductSqlLiteRepository(conn)

        for product in product_list:
            repo.create(product)

        new_list = repo.get_all()
        assert len(new_list) == len(product_list)
        for i in range(len(product_list)):
            check_equality(new_list[i], product_list[i])

        conn.close()

    def test_should_update_product_price(self, conn: Connection) -> None:
        prod = Product("1", "1", "1", "11", 520)
        repo = ProductSqlLiteRepository(conn)
        repo.create(prod)

        repo.update("1", 20)
        check_equality(repo.get("1"), prod)
