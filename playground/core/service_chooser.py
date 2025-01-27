from playground.core.product import IProductService, ProductRepository, ProductService
from playground.core.receipt import IReceiptService, ReceiptRepository, ReceiptService
from playground.core.sales import ISalesService, SalesService
from playground.core.unit import IUnitService, UnitRepository, UnitService


class ServiceChooser:
    def __init__(self) -> None:
        self.product_service = ProductService
        self.receipt_service = ReceiptService
        self.unit_service = UnitService
        self.sale_service = SalesService

    def product_service_class(self, repo: ProductRepository) -> IProductService:
        return self.product_service(repo)

    def receipt_service_class(self, repo: ReceiptRepository) -> IReceiptService:
        return self.receipt_service(repo)

    def unit_service_class(self, repo: UnitRepository) -> IUnitService:
        return self.unit_service(repo)

    def sales_service_class(self, repo: ReceiptRepository) -> ISalesService:
        return self.sale_service(repo)
