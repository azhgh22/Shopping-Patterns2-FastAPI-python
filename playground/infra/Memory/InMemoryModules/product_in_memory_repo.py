import copy

from playground.core.product import Product


class ProductInMemoryRepository:
    def __init__(self, init_list: list[Product] | None = None) -> None:
        if init_list is None:
            init_list = []
        self._product_list: list[Product] = init_list

    def create(self, prod: Product) -> None:
        self._product_list.append(copy.copy(prod))

    def __get_in_memory_product_with_id(self, product_id: str) -> Product | None:
        for prod in self._product_list:
            if prod.id == product_id:
                return prod

        return None

    def get(self, product_id: str) -> Product | None:
        return copy.deepcopy(self.__get_in_memory_product_with_id(product_id))

    def get_all(self) -> list[Product]:
        return copy.deepcopy(self._product_list)

    def get_with_barcode(self, barcode: str) -> Product | None:
        for prod in self._product_list:
            if prod.barcode == barcode:
                return copy.copy(prod)

        return None

    def update(self, prod_id: str, price: int) -> None:
        prod = self.__get_in_memory_product_with_id(prod_id)
        if prod is not None:
            prod.price = price
