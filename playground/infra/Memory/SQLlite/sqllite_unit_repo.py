from sqlite3 import Connection

from playground.core.unit import Unit


class UnitSqlLiteRepository:
    def __init__(self, conn: Connection):
        self.connection = conn
        self.__create_unit_table()

    def __create_unit_table(self) -> None:
        self.connection.execute("""
                                    CREATE TABLE IF NOT EXISTS units(
                                        id Text,
                                        unit_name Text    
                                    ); """)

        self.connection.commit()

    def create_unit(self, unit: Unit) -> None:
        self.connection.execute(
            """
            insert into units(id,unit_name)
            values(?,?);
            """,
            (unit.id, unit.name),
        )

        self.connection.commit()

    def __unit_with_parameter(self, key: str, value: str) -> list[Unit]:
        raw = self.connection.execute(
            f"""
            select * from units where {key} = '{value}';
        """
        ).fetchall()
        return list(Unit(x[0], x[1]) for x in raw)

    def get_unit(self, unit_id: str) -> Unit | None:
        units = self.__unit_with_parameter("id", unit_id)
        if len(units) == 0:
            return None
        return units[0]

    def get_all_units(self) -> list[Unit]:
        return self.__unit_with_parameter('"1"', "1")

    def get_unit_with_name(self, unit_name: str) -> Unit | None:
        units = self.__unit_with_parameter("unit_name", unit_name)
        if len(units) == 0:
            return None
        return units[0]
