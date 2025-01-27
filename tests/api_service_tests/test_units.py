from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from playground.core.unit import Unit, UnitService
from playground.infra.Memory.InMemoryModules.unit_in_memory_repo import (
    UnitInMemoryRepository,
)
from playground.runner.setup import MemoryType, setup


class TestUnits:
    @pytest.fixture
    def http(self) -> TestClient:
        return TestClient(setup(MemoryType.IN_MEMORY))

    def test_environment_works(self) -> None:
        pass

    def test_should_read_empty_list_of_units(self, http: TestClient) -> None:
        response = http.get("/units")
        assert response.status_code == 200
        assert response.json() == []

    def test_should_return_404_http(self, http: TestClient) -> None:
        unit_id = 1234
        response = http.get(f"units/{unit_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Unit with id<{unit_id}> does not exist."

    def test_should_create_new_unit(self, http: TestClient) -> None:
        new_unit = {"name": "kg"}
        response = http.post("/units", json=new_unit)
        assert response.status_code == 201
        assert response.json() == {"id": ANY, **new_unit}

    def test_service_should_return_unit(self) -> None:
        unit_list = [Unit("1", "a")]
        service = UnitService(UnitInMemoryRepository(unit_list))
        ret_val = service.get_unit("1")
        assert ret_val is not None and ret_val.name == unit_list[0].name

    def test_should_persist_new_unit(self, http: TestClient) -> None:
        new_unit = {"name": "kg"}
        unit_id = http.post("/units", json=new_unit).json()["id"]
        response = http.get(f"units/{unit_id}")
        assert response.status_code == 200
        assert response.json() == {"id": unit_id, **new_unit}

    def test_unit_service_should_add_new_unit(self) -> None:
        unit_list: list[Unit] = []
        unit_service = UnitService(UnitInMemoryRepository(unit_list))
        new_unit = unit_service.create_unit("free uni")
        assert new_unit is not None and unit_list[0].name == new_unit.name

    def test_should_return_409_error(self, http: TestClient) -> None:
        unit = {"name": "kg"}
        http.post("/units", json=unit)
        response = http.post("/units", json=unit)
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == f"Unit with name {unit["name"]} already exists."
        )

    def test_service_should_return_all_units(self) -> None:
        unit_list = [Unit("1", "a")]
        service = UnitService(UnitInMemoryRepository(unit_list))
        ret_list = service.get_all_units()
        assert len(ret_list) == 1
        assert ret_list[0].name == unit_list[0].name

    def test_should_return_list_of_units(self, http: TestClient) -> None:
        unit1 = {"name": "unit1"}
        unit2 = {"name": "unit2"}
        http.post("/units", json=unit1)
        http.post("/units", json=unit2)
        response = http.get("/units")
        assert response.status_code == 200
        assert len(response.json()) == 2
