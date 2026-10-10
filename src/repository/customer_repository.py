from database.connection import get_connection
from model.customer import Customer

class CustomerRepository:

    ALLOWED_FIELDS = ("first_name", "last_name", "email", "city", "country", "phone", "postal_code")

    @staticmethod
    def _row_to_customer(row):
        return Customer(
            customer_id = row["customer_id"],
            first_name = row["first_name"],
            last_name = row["last_name"],
            email = row["email"],
            city = row["city"],
            country = row["country"],
            phone = row["phone"],
            postal_code = row["postal_code"]
        )


    def create(self, customer):
        query = """
            Insert Into customers
                (first_name, last_name, email, city, country, phone, postal_code)
            Values(%s, %s, %s, %s, %s, %s, %s)
            """
        params = (
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.city,
            customer.country,
            customer.phone,
            customer.postal_code
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


    def search_by_id(self, customer_id):
        query = """
            Select * From customers
            Where customer_id =  %s
            """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()
            return self._row_to_customer(row) if row else None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def search_by_email(self, email):
        query = """
            Select * From customers
            Where email = %s """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (email, ))
            row = cursor.fetchone()
            return self._row_to_customer(row) if row else None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_all_customers(self):
        query = """
            Select * From customers
            """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            all_customers = [self._row_to_customer(row) for row in rows]
            return all_customers

        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            

    def delete_customer(self, customer_id):
        query = """
            Delete From customers
            Where customer_id = %s
            """

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (customer_id, ))
            conn.commit()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def update_customer(self, customer_id, field, new_value):

        if field not in self.allowed_fields:
            raise ValueError(f"Invalid field: {field}")

        query = f"""
            Update customers
            Set {field} = %s
            where customer_id = %s"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (new_value, customer_id))
            conn.commit()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        