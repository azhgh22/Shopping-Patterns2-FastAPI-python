import sqlite3

from playground.core.product import ProductRepository
from playground.core.receipt import ReceiptRepository
from playground.core.unit import UnitRepository
from playground.infra.Memory.SQLlite.sqllite_product_repo import (
    ProductSqlLiteRepository,
)
from playground.infra.Memory.SQLlite.sqllite_receipt_repo import (
    ReceiptSqlLiteRepository,
)
from playground.infra.Memory.SQLlite.sqllite_unit_repo import UnitSqlLiteRepository


class SqlLite:
    def __init__(self) -> None:
        connection = sqlite3.connect("shop.db", check_same_thread=False)
        self._units = UnitSqlLiteRepository(connection)
        self._products = ProductSqlLiteRepository(connection)
        self._receipts = ReceiptSqlLiteRepository(connection)

    def unit_repository(self) -> UnitRepository:
        return self._units

    def product_repository(self) -> ProductRepository:
        return self._products

    def receipt_repository(self) -> ReceiptRepository:
        return self._receipts
