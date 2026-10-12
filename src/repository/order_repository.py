from database.connection import get_connection
from model.order import Order

class OrderRepository:

    @staticmethod
    def _row_to_order(row):
        return Order(
            order_id = row["order_id"],
            customer_id = row["customer_id"],
            order_date = row["order_date"],
            total_price = row["total_price"]
        )

    def create(self, order, cursor):
        query = """
            Insert Into orders(customer_id, order_date, total_price)
            Values(%s, %s, %s)
        """
        params = (
            order.customer_id,
            order.order_date,
            order.total_price
            )

        cursor.execute(query, params)
        return cursor.lastrowid

    def search_by_order_id(self, order_id):
        query = """
            Select * From orders
            Where order_id = %s
        """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (order_id, ))
            row = cursor.fetchone()
            return self._row_to_order(row) if row else None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def search_by_customer_id(self, customer_id):
        query = """
            Select * From orders
            Where customer_id = %s
        """


        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (customer_id, ))
            rows = cursor.fetchall()
            all_orders = [self._row_to_order(row) for row in rows ]
            return all_orders
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_all_orders(self):
        query = """
            Select * From orders
        """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            all_orders = [self._row_to_order(row) for row in rows]
            return all_orders
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
