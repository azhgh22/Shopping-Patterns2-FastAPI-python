from sqlite3 import Connection

from playground.core.product import Product


class ProductSqlLiteRepository:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.__create_product_table()

    def __create_product_table(self) -> None:
        self.conn.execute("""
            create table if not exists products (
                id Text,
                unit_id Text,
                product_name Text,
                barcode Text,
                price Integer
            )
        """)
        self.conn.commit()

    def create(self, product: Product) -> None:
        self.conn.execute(
            """
        insert into products (id, unit_id, product_name, barcode, price)
        values (?,?,?,?,?)
         """,
            (product.id, product.unit_id, product.name, product.barcode, product.price),
        )

    def __get_with_param(self, key: str, value: str) -> list[Product]:
        raw = self.conn.execute(f"""
            select * from products where {key} = '{value}'
        """).fetchall()

        return list(Product(x[0], x[1], x[2], x[3], x[4]) for x in raw)

    def get(self, product_id: str) -> Product | None:
        product_list = self.__get_with_param("id", product_id)
        if len(product_list) == 0:
            return None
        return product_list[0]

    def get_all(self) -> list[Product]:
        return self.__get_with_param('"1"', "1")

    def get_with_barcode(self, barcode: str) -> Product | None:
        product_list = self.__get_with_param("barcode", barcode)
        if len(product_list) == 0:
            return None
        return product_list[0]

    def update(self, prod_id: str, price: int) -> None:
        pass
