import copy

from playground.core.unit import Unit


class UnitInMemoryRepository:
    def __init__(self, init_list: list[Unit] | None = None) -> None:
        if init_list is None:
            init_list = []
        self._unit_list: list[Unit] = init_list

    def create_unit(self, unit: Unit) -> None:
        self._unit_list.append(copy.copy(unit))

    def get_unit(self, unit_id: str) -> Unit | None:
        for unit in self._unit_list:
            if unit.id == unit_id:
                return copy.copy(unit)

        return None

    def get_all_units(self) -> list[Unit]:
        return copy.deepcopy(self._unit_list)

    def get_unit_with_name(self, unit_name: str) -> Unit | None:
        for unit in self._unit_list:
            if unit.name == unit_name:
                return copy.copy(unit)

        return None
