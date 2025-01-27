from sqlite3 import Connection

from playground.core.product import Product
from playground.core.receipt import ProductInReceipt, Receipt, Sales


class ReceiptSqlLiteRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        self.__create_receipt_table()
        self.__create_receipt_product_linker_table()

    def create(self, new_receipt: Receipt) -> None:
        self.conn.execute(
            """
            insert into receipts(id,status,total)
            values (?,?,?)
        """,
            (new_receipt.id, new_receipt.status, new_receipt.total),
        )

        self.conn.commit()

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        receipt_object = self.__fill_with_receipt_meta_data(receipt_id)
        if receipt_object is None:
            return None

        self.__fill_receipt_object_with_products(receipt_object)
        return receipt_object

    def add_product_to_receipt(
        self, product_info: ProductInReceipt, receipt_id: str
    ) -> None:
        self.conn.execute(
            """
            insert into receipt_product_linker(receipt_id,product_id,quantity)
            values (?,?,?)
        """,
            (receipt_id, product_info.product.id, product_info.quantity),
        )
        self.conn.commit()

    def update_status(self, receipt_id: str, new_status: str) -> bool:
        row_count = self.conn.execute(
            """
            update receipts
            set status=?
            where id=?
        """,
            (new_status, receipt_id),
        ).rowcount

        return row_count == 1

    def remove(self, receipt_id: str) -> None:
        self.conn.execute(f"""
            delete from receipt_product_linker
            where receipt_id='{receipt_id}'
        """)

        self.conn.execute(f"""
                    delete from receipts
                    where id='{receipt_id}'
                """)

    def get_sales_info(self) -> Sales:
        raw = self.conn.execute("""
            select count(*),sum(total) from receipts
        """).fetchone()

        return Sales(raw[0], raw[1])

    def receipt_has_product(self, product_id: str, receipt_id: str) -> bool:
        raw = self.conn.execute(
            """
            select count(*) from receipt_product_linker
            where product_id=? and receipt_id=?
        """,
            (product_id, receipt_id),
        ).fetchone()

        if raw[0] == 1:
            return True
        return False

    def increase_receipt_total(self, receipt_id: str, increase: int) -> None:
        self.conn.execute(
            """
            update receipts
            set total= total + ?
            where id=?
        """,
            (increase, receipt_id),
        )

    def __create_receipt_table(self) -> None:
        self.conn.execute("""
            create table if not exists receipts(
                id Text,
                status Text,
                total Integer
            )
        """)

        self.conn.commit()

    def __create_receipt_product_linker_table(self) -> None:
        self.conn.execute("""
            create table if not exists receipt_product_linker(
                receipt_id Text,
                product_id Text,
                quantity Integer
            )
        """)

        self.conn.commit()

    def __fill_with_receipt_meta_data(self, receipt_id: str) -> Receipt | None:
        raw = self.conn.execute(f"""
            select * from receipts
            where id='{receipt_id}';
        """).fetchone()

        if raw is None:
            return None

        return Receipt(raw[0], raw[1], [], raw[2])

    def __fill_receipt_object_with_products(self, receipt: Receipt) -> None:
        raw = self.conn.execute(f"""
            select l.quantity, p.id,p.unit_id,p.product_name,p.barcode,p.price 
            from receipt_product_linker l
            left join products p
            on l.product_id = p.id
            where l.receipt_id = '{receipt.id}';
        """).fetchall()

        for r in raw:
            receipt.products.append(
                ProductInReceipt(Product(r[1], r[2], r[3], r[4], r[5]), r[0])
            )
