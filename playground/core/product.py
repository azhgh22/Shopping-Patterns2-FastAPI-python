import uuid
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Product:
    id: str
    unit_id: str
    name: str
    barcode: str
    price: int


class ProductRepository(Protocol):
    def create(self, product: Product) -> None:
        pass

    def get(self, product_id: str) -> Product | None:
        pass

    def get_all(self) -> list[Product]:
        pass

    def get_with_barcode(self, barcode: str) -> Product | None:
        pass

    def update(self, prod_id: str, price: int) -> bool:
        pass


@dataclass
class ProductCreateRequestModel:
    unit_id: str
    name: str
    barcode: str
    price: int


class IProductService(Protocol):
    def create(self, input_prod: ProductCreateRequestModel) -> Product | None:
        pass

    def get_all(self) -> list[Product]:
        pass

    def get(self, product_id: str) -> Product | None:
        pass

    def update(self, prod_id: str, price: int) -> bool:
        pass


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create(self, input_prod: ProductCreateRequestModel) -> Product | None:
        if self.repository.get_with_barcode(input_prod.barcode) is not None:
            return None

        product = Product(
            str(uuid.uuid3(uuid.NAMESPACE_DNS, "shop.ge")),
            input_prod.unit_id,
            input_prod.name,
            input_prod.barcode,
            input_prod.price,
        )
        self.repository.create(product)
        return product

    def get_all(self) -> list[Product]:
        return self.repository.get_all()

    def get(self, product_id: str) -> Product | None:
        prod = self.repository.get(product_id)
        return prod

    def update(self, prod_id: str, price: int) -> bool:
        return self.repository.update(prod_id, price)
