from fastapi import APIRouter
from starlette.requests import Request

from playground.core.sales import ISalesService
from playground.core.service_chooser import ServiceChooser

sales_router = APIRouter()


def get_sales_core(request: Request) -> ISalesService:
    service_chooser: ServiceChooser = request.app.state.core
    return service_chooser.sales_service_class(
        request.app.state.infra.receipt_repository()
    )


@sales_router.get("/", status_code=200)
def get_sales(request: Request) -> dict[str, int]:
    service = get_sales_core(request)
    return service.get_sales()
