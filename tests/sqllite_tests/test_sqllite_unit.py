import os
import sqlite3
from sqlite3 import Connection

import pytest

from playground.core.unit import Unit
from playground.infra.Memory.SQLlite.sqllite_unit_repo import UnitSqlLiteRepository


def check_equality(unit1: Unit | None, unit2: Unit) -> None:
    assert unit1 is not None
    assert unit1.id == unit2.id
    assert unit1.name == unit2.name


class TestUnitSqlLite:
    @pytest.fixture
    def conn(self) -> Connection:
        file_path = "shop_test.db"
        if os.path.exists(file_path):
            os.remove(file_path)
        return sqlite3.connect(file_path, check_same_thread=False)

    def test_should_store_new_unit(self, conn: Connection) -> None:
        repo = UnitSqlLiteRepository(conn)
        unit = Unit("1", "1st")
        repo.create_unit(unit)

        raw = conn.execute("select * from units").fetchall()

        assert len(raw) == 1
        assert raw[0][0] == "1"
        assert raw[0][1] == "1st"

        conn.close()

    def test_should_get_unit_with_id(self, conn: Connection) -> None:
        repo = UnitSqlLiteRepository(conn)
        unit = Unit("1", "1st")
        repo.create_unit(unit)

        res = repo.get_unit("1")
        check_equality(res, unit)
        conn.close()

    def test_should_get_unit_with_name(self, conn: Connection) -> None:
        repo = UnitSqlLiteRepository(conn)
        unit = Unit("1", "1st")
        repo.create_unit(unit)

        res = repo.get_unit_with_name("1st")
        check_equality(res, unit)
        conn.close()

    def test_should_get_all_units(self, conn: Connection) -> None:
        repo = UnitSqlLiteRepository(conn)
        unit1 = Unit("1", "1st")
        unit2 = Unit("2", "2nd")
        repo.create_unit(unit1)
        repo.create_unit(unit2)

        units = repo.get_all_units()
        assert len(units) == 2
        check_equality(units[0], unit1)
        check_equality(units[1], unit2)
        conn.close()
