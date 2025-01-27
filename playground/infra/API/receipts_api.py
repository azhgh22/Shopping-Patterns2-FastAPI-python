from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from playground.core.receipt import (
    AddProductInput,
    IReceiptService,
    Receipt,
    RemoveResults,
)
from playground.core.service_chooser import ServiceChooser
from playground.infra.API.products_api import get_product_core

receipts_router = APIRouter()


def get_receipt_core(request: Request) -> IReceiptService:
    service_chooser: ServiceChooser = request.app.state.core
    return service_chooser.receipt_service_class(
        request.app.state.infra.receipt_repository()
    )


# Create
@receipts_router.post("/", status_code=201)
def create_receipt(request: Request) -> Receipt:
    service = get_receipt_core(request)
    return service.create()


# Get one
@receipts_router.get("/{receipt_id}", status_code=200)
def get_receipt(receipt_id: str, request: Request) -> Receipt:
    service = get_receipt_core(request)
    receipt = service.get_receipt(receipt_id)
    if receipt is None:
        raise HTTPException(
            status_code=404, detail=f"Receipt with id<{receipt_id}> does not exist."
        )
    return receipt


class AddModel(BaseModel):
    id: str
    quantity: int


# Add Product
@receipts_router.post("/{receipt_id}/products", status_code=201)
def add_product(receipt_id: str, info: AddModel, request: Request) -> dict[str, Any]:
    service = get_receipt_core(request)
    receipt = service.add_product(
        AddProductInput(info.id, info.quantity, receipt_id), get_product_core(request)
    )
    print(info.id, info.quantity, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="Receipt or Product not found")

    return receipt


class CloseActionInputModel(BaseModel):
    status: str


# Close Receipt
@receipts_router.patch("/{receipt_id}", status_code=200)
def close_receipt(
    receipt_id: str, info: CloseActionInputModel, request: Request
) -> None:
    service = get_receipt_core(request)
    if not service.close_receipt(receipt_id, info.status):
        raise HTTPException(
            status_code=404, detail=f"Receipt with id<{receipt_id}> does not exist."
        )


# Delete Receipt
@receipts_router.delete("/{receipt_id}", status_code=200)
def delete_receipt(receipt_id: str, request: Request) -> None:
    service = get_receipt_core(request)
    status = service.delete_receipt(receipt_id)
    if status == RemoveResults.RECEIPT_NOT_FOUND:
        raise HTTPException(
            status_code=404, detail=f"Receipt with id<{receipt_id}> does not exist."
        )
    elif status == RemoveResults.RECEIPT_CLOSED:
        raise HTTPException(
            status_code=403, detail=f"Receipt with id<{receipt_id}> is closed."
        )
