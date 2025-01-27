from playground.core.product import ProductRepository
from playground.core.receipt import (
    ReceiptRepository,
)
from playground.core.unit import UnitRepository
from playground.infra.Memory.InMemoryModules.product_in_memory_repo import (
    ProductInMemoryRepository,
)
from playground.infra.Memory.InMemoryModules.receipt_in_memory_repo import (
    ReceiptInMemoryRepository,
)
from playground.infra.Memory.InMemoryModules.unit_in_memory_repo import (
    UnitInMemoryRepository,
)


class InMemory:
    def __init__(self) -> None:
        self._units = UnitInMemoryRepository()
        self._products = ProductInMemoryRepository()
        self._receipts = ReceiptInMemoryRepository()

    def unit_repository(self) -> UnitRepository:
        return self._units

    def product_repository(self) -> ProductRepository:
        return self._products

    def receipt_repository(self) -> ReceiptRepository:
        return self._receipts
