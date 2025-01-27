import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

from playground.core.product import IProductService, Product


@dataclass
class Sales:
    n_receipts: int
    total: int


@dataclass
class ProductInReceipt:
    product: Product
    quantity: int


@dataclass
class Receipt:
    id: str
    status: str
    products: list[ProductInReceipt]
    total: int


@dataclass
class AddProductInput:
    product_id: str
    quantity: int
    receipt_id: str


class ReceiptRepository(Protocol):
    def create(self, new_receipt: Receipt) -> None:
        pass

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        pass

    def add_product_to_receipt(
        self, product_info: ProductInReceipt, receipt_id: str
    ) -> None:
        pass

    def update_status(self, receipt_id: str, new_status: str) -> bool:
        pass

    def remove(self, receipt_id: str) -> None:
        pass

    def get_sales_info(self) -> Sales:
        pass

    def increase_receipt_total(self, receipt_id: str, increase: int) -> None:
        pass

    def receipt_has_product(self, product_id: str, receipt_id: str) -> bool:
        pass


class ReceiptFormater:
    def __init__(self, receipt: Receipt | None) -> None:
        self.receipt = receipt

    def json(self) -> dict[str, Any] | None:
        if self.receipt is None:
            return None
        return {
            "id": self.receipt.id,
            "status": self.receipt.status,
            "products": list(
                (
                    {
                        "quantity": x.quantity,
                        "id": x.product.id,
                        "price": x.product.price,
                        "total": x.product.price * x.quantity,
                    }
                    for x in self.receipt.products
                )
            ),
            "total": self.receipt.total,
        }


class RemoveResults(Enum):
    RECEIPT_REMOVED = 0
    RECEIPT_CLOSED = 1
    RECEIPT_NOT_FOUND = 2


class IReceiptService(Protocol):
    def create(self) -> Receipt:
        pass

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        pass

    def add_product(
        self, info: AddProductInput, product_service: IProductService
    ) -> dict[str, Any] | None:
        pass

    def close_receipt(self, receipt_id: str, new_status: str) -> bool:
        pass

    def delete_receipt(self, receipt_id: str) -> RemoveResults:
        pass


class ReceiptService:
    def __init__(self, repository: ReceiptRepository):
        self.repository = repository

    def create(self) -> Receipt:
        new_receipt = Receipt(
            str(uuid.uuid3(uuid.NAMESPACE_DNS, "shop.ge")), "open", [], 0
        )
        self.repository.create(new_receipt)
        return new_receipt

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        return self.repository.get_receipt(receipt_id)

    def add_product(
        self, info: AddProductInput, product_service: IProductService
    ) -> dict[str, Any] | None:
        prod = product_service.get(info.product_id)
        if prod is None:
            return None
        if not self.repository.receipt_has_product(info.product_id, info.receipt_id):
            self.__add_new_product(prod, info)
        increase = info.quantity * prod.price
        self.repository.increase_receipt_total(info.receipt_id, increase)
        return ReceiptFormater(self.repository.get_receipt(info.receipt_id)).json()

    def close_receipt(self, receipt_id: str, new_status: str) -> bool:
        return self.repository.update_status(receipt_id, new_status)

    def delete_receipt(self, receipt_id: str) -> RemoveResults:
        receipt = self.repository.get_receipt(receipt_id)
        if receipt is None:
            return RemoveResults.RECEIPT_NOT_FOUND

        if receipt.status == "closed":
            return RemoveResults.RECEIPT_CLOSED

        self.repository.remove(receipt_id)
        return RemoveResults.RECEIPT_REMOVED

    def __add_new_product(self, prod: Product, info: AddProductInput) -> None:
        prod_in_receipt = ProductInReceipt(prod, info.quantity)
        self.repository.add_product_to_receipt(prod_in_receipt, info.receipt_id)
