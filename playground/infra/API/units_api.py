from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from playground.core.service_chooser import ServiceChooser
from playground.core.unit import IUnitService, Unit

units_router = APIRouter()


def get_unit_core(request: Request) -> IUnitService:
    service_chooser: ServiceChooser = request.app.state.core
    return service_chooser.unit_service_class(request.app.state.infra.unit_repository())


# List
@units_router.get("/", status_code=200)
def get_units(request: Request) -> list[Unit]:
    unit_service = get_unit_core(request)
    return unit_service.get_all_units()


# Read one
@units_router.get("/{unit_id}", status_code=200)
def get_unit(unit_id: str, request: Request) -> Unit:
    unit_service = get_unit_core(request)
    unit = unit_service.get_unit(unit_id)
    if unit is None:
        raise HTTPException(
            status_code=404, detail=f"Unit with id<{unit_id}> does not exist."
        )
    return unit


class UnitCreateRequest(BaseModel):
    name: str


# Create
@units_router.post("/", status_code=201)
def create_unit(req: UnitCreateRequest, request: Request) -> Unit:
    unit_service = get_unit_core(request)
    unit = unit_service.create_unit(req.name)
    if unit is None:
        raise HTTPException(
            status_code=409, detail=f"Unit with name {req.name} already exists."
        )
    return unit
