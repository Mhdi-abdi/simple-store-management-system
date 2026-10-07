from database.connection import get_connection
from model.product import Product

class ProductRepository:

    @staticmethod
    def _row_to_product(row):
        return Product(
            product_id = row["product_id"],
            product_name = row["product_name"],
            price = row["price"],
            stock_quantity = row["stock_quantity"],
            description = row["description"],
            is_active = row["is_active"]
        )

    def create(self, product):
        query = """
            Insert Into products(product_name, price, stock_quantity, description, is_active)
            Values(%s, %s, %s, %s, %s)
            """
        params = (
            product.product_name,
            product.price,
            product.stock_quantity,
            product.description,
            product.is_active
        )

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def search_by_product_id(self, product_id):
        query = """
            Select * From products
            Where product_id = %s 
            """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (product_id, ))
            row = cursor.fetchone()
            return self._row_to_product(row) if row else None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def search_by_name(self, product_name):
        query = """
            Select * From products
            Where product_name = %s
            """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (product_name, ))
            row = cursor.fetchone()
            return self._row_to_product(row) if row else None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_all_products(self):
        query = """ 
            Select * From products
            """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            all_product = [self._row_to_product(row) for row in rows]
            return all_product

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_product_description(self, product_id):
        query = """
            Select description From products
            Where product_id = %s
            """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (product_id, ))
            row = cursor.fetchone()
            return row["description"] if row else None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def update_product(self, product_id, field, new_value):
        query = f"""
            Update products
            set {field} = %s
            where product_id = %s
        """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (new_value, product_id))
            conn.commit()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def toggle_product_status(self, product_id, new_value):
        query = """
            update products
            Set is_active = %s
            Where product_id = %s
        """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (new_value, product_id))
            conn.commit()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
