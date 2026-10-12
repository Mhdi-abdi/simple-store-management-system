from database.connection import get_connection
from model.order_item import OrderItem

class OrderItemRepository:

    @staticmethod
    def _row_to_order_item(row):
        return OrderItem(
            order_item_id = row["order_item_id"],
            order_id = row["order_id"],
            product_id = row["product_id"],
            unit_price = row["unit_price"],
            quantity = row["quantity"]
        )


    def create(self, order_items, cursor):
        query = """
            Insert Into order_items(order_id, product_id, unit_price, quantity)
            Values(%s, %s, %s, %s)
        """
        
        params = [
            (order_item.order_id,
            order_item.product_id,
            order_item.unit_price,
            order_item.quantity) for order_item in order_items]


        cursor.executemany(query, params)


    def search_by_order_item_id(self, order_item_id):
        query = """
            Select * From order_items
            Where order_item_id = %s
        """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (order_item_id, ))
            row = cursor.fetchone()
            return self._row_to_order_item(row) if row else None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def search_by_order_id(self, order_id):
        query = """
            Select * From order_items
            Where order_id = %s
        """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (order_id, ))
            rows = cursor.fetchall()
            all_order_items = [self._row_to_order_item(row) for row in rows ] 
            return all_order_items

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_order_items(self):
        query = """
            Select * From order_items
        """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            all_order_items = [self._row_to_order_item(row) for row in rows ] 
            return all_order_items

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
