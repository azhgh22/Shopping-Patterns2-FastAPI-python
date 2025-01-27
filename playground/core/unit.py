import uuid
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Unit:
    id: str
    name: str


class UnitRepository(Protocol):
    def create_unit(self, unit: Unit) -> None:
        pass

    def get_unit(self, unit_id: str) -> Unit | None:
        pass

    def get_all_units(self) -> list[Unit]:
        pass

    def get_unit_with_name(self, unit_name: str) -> Unit | None:
        pass


class IUnitService(Protocol):
    def create_unit(self, unit_name: str) -> Unit | None:
        pass

    def get_all_units(self) -> list[Unit]:
        pass

    def get_unit(self, unit_id: str) -> Unit | None:
        pass


class UnitService:
    def __init__(self, repo: UnitRepository):
        self.unit_repository = repo

    def create_unit(self, unit_name: str) -> Unit | None:
        unit = self.unit_repository.get_unit_with_name(unit_name)
        if unit is not None:
            return None

        new_unit = Unit(str(uuid.uuid3(uuid.NAMESPACE_DNS, "shop.ge")), unit_name)
        self.unit_repository.create_unit(new_unit)
        return new_unit

    def get_all_units(self) -> list[Unit]:
        return self.unit_repository.get_all_units()

    def get_unit(self, unit_id: str) -> Unit | None:
        unit = self.unit_repository.get_unit(unit_id)
        return unit
