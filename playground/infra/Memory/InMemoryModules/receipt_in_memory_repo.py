import copy

from playground.core.receipt import ProductInReceipt, Receipt, Sales


class ReceiptInMemoryRepository:
    def __init__(self, init_list: list[Receipt] | None = None):
        if init_list is None:
            init_list = []
        self._receipt_list = init_list

    def create(self, new_receipt: Receipt) -> None:
        self._receipt_list.append(copy.deepcopy(new_receipt))

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        return copy.deepcopy(self.__get_in_memory_receipt(receipt_id))

    def add_product_to_receipt(
        self, product_info: ProductInReceipt, receipt_id: str
    ) -> None:
        receipt = self.__get_in_memory_receipt(receipt_id)
        if receipt is None:
            return None
        receipt.products.append(copy.deepcopy(product_info))

    def update_status(self, receipt_id: str, new_status: str) -> bool:
        receipt = self.__get_in_memory_receipt(receipt_id)
        if receipt is None:
            return False
        receipt.status = new_status
        return True

    def __get_in_memory_receipt(self, receipt_id: str) -> Receipt | None:
        for receipt in self._receipt_list:
            if receipt.id == receipt_id:
                return receipt

        return None

    def remove(self, receipt_id: str) -> None:
        receipt = self.__get_in_memory_receipt(receipt_id)
        if receipt is not None:
            self._receipt_list.remove(receipt)

    @staticmethod
    def __get_in_memory_product(
        receipt: Receipt, product_id: str
    ) -> ProductInReceipt | None:
        for product in receipt.products:
            if product.product.id == product_id:
                return product

        return None

    def get_sales_info(self) -> Sales:
        n = len(self._receipt_list)
        total = 0
        for receipt in self._receipt_list:
            total += receipt.total

        return Sales(n, total)

    def increase_receipt_total(self, receipt_id: str, increase: int) -> None:
        for receipt in self._receipt_list:
            if receipt.id == receipt_id:
                receipt.total += increase

    def receipt_has_product(self, product_id: str, receipt_id: str) -> bool:
        receipt = self.__get_in_memory_receipt(receipt_id)
        if receipt is None:
            return False
        product = self.__get_in_memory_product(receipt, product_id)
        if product is None:
            return False
        return True
