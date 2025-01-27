from typing import Protocol

from playground.core.receipt import ReceiptRepository, Sales


class ISalesService(Protocol):
    def get_sales(self) -> dict[str, int]:
        pass


class SalesFormater:
    def __init__(self, receipts_list: Sales):
        self.receipts = receipts_list

    def json(self) -> dict[str, int]:
        return {"n_receipts": self.receipts.n_receipts, "revenue": self.receipts.total}


class SalesService:
    def __init__(self, receipts_repository: ReceiptRepository):
        self.repository = receipts_repository

    def get_sales(self) -> dict[str, int]:
        sales_info = self.repository.get_sales_info()
        return SalesFormater(sales_info).json()
