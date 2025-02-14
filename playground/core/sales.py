from typing import Any, Protocol

from playground.core.receipt import ReceiptRepository, Sales


class ISalesService(Protocol):
    def get_sales(self) -> dict[str, int]:
        pass


class SalesFormaterI(Protocol):
    def json(self, receipts: Sales) -> dict[str, Any]:
        pass


class SalesFormater:
    def json(self, receipts: Sales) -> dict[str, Any]:
        return {"n_receipts": receipts.n_receipts, "revenue": receipts.total}


class SalesService:
    def __init__(
        self,
        receipts_repository: ReceiptRepository,
        formater: SalesFormaterI = SalesFormater(),
    ):
        self.repository = receipts_repository
        self.formater = formater

    def get_sales(self) -> dict[str, Any]:
        sales_info = self.repository.get_sales_info()
        return self.formater.json(sales_info)
