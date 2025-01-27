from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from playground.core.product import IProductService, Product, ProductCreateRequestModel
from playground.core.service_chooser import ServiceChooser

product_router = APIRouter()


def get_product_core(request: Request) -> IProductService:
    service_chooser: ServiceChooser = request.app.state.core
    return service_chooser.product_service_class(
        request.app.state.infra.product_repository()
    )


# List
@product_router.get("/", status_code=200)
def get_product_list(request: Request) -> list[Product]:
    service = get_product_core(request)
    return service.get_all()


# Create
@product_router.post("/", status_code=201)
def create_product(data: ProductCreateRequestModel, request: Request) -> Product:
    service = get_product_core(request)
    product = service.create(data)
    if product is None:
        raise HTTPException(
            status_code=409,
            detail=f"Product with barcode<{data.barcode}> already exists.",
        )
    return product


# Get One
@product_router.get("/{product_id}", status_code=200)
def get_product(request: Request, product_id: str) -> Product:
    service = get_product_core(request)
    product = service.get(product_id)
    if product is None:
        raise HTTPException(
            status_code=404, detail=f"Product with id<{product_id}> does not exist."
        )
    return product


class UpdateModel(BaseModel):
    price: int


# Update
@product_router.patch("/{product_id}", status_code=200)
def update_product(request: Request, product_id: str, data: UpdateModel) -> None:
    service = get_product_core(request)
    res = service.update(product_id, data.price)
    if res is False:
        raise HTTPException(
            status_code=409, detail=f"Product with id<{product_id}> does not exist."
        )
