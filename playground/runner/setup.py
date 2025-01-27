import enum

from fastapi import FastAPI

from playground.core.service_chooser import ServiceChooser
from playground.infra.API.products_api import product_router
from playground.infra.API.receipts_api import receipts_router
from playground.infra.API.sales_api import sales_router
from playground.infra.API.units_api import units_router
from playground.infra.Memory.InMemoryModules.in_memory import InMemory
from playground.infra.Memory.SQLlite.sql_lite import SqlLite


class MemoryType(enum.Enum):
    IN_MEMORY = 0
    SQL_LITE = 1


def setup(memory_type: MemoryType) -> FastAPI:
    api = FastAPI()
    api.state.infra = InMemory()
    if memory_type == MemoryType.SQL_LITE:
        api.state.infra = SqlLite()
    service = ServiceChooser()
    api.state.core = service
    api.include_router(units_router, prefix="/units", tags=["Units"])
    api.include_router(product_router, prefix="/products", tags=["Products"])
    api.include_router(receipts_router, prefix="/receipts", tags=["Receipts"])
    api.include_router(sales_router, prefix="/sales", tags=["Sales"])
    return api
