from decimal import Decimal
from datetime import datetime

from src.model.order import Order
from src.model.order_item import OrderItem
from src.repository.customer_repository import CustomerRepository
from src.repository.product_repository import ProductRepository
from src.repository.order_repository import OrderRepository
from src.repository.order_item_repository import OrderItemRepository
from src.exceptions import ValidationError, InsufficientStockError, NotFoundError
from src.database.connection import get_connection

class OrderService:

    MAX_QUANTITY = 2147483647

    def __init__(self):
        self.customer_repo = CustomerRepository()
        self.product_repo = ProductRepository()
        self.order_repo = OrderRepository()
        self.item_repo = OrderItemRepository()


    @classmethod
    def _parse_quantity(cls, value):
        try:
            value = int(str(value).strip())
        except ValueError:
            raise ValidationError("quantity must be number")
        if value > cls.MAX_QUANTITY:
            raise ValidationError("quantity is too large!")
        if value <= 0:
            raise ValidationError("quantity must be greater than zero")
        return value

    def merge_items(self, items):
        merged = {}
        for product_id , quantity in items:
            try:
                product_id = int(str(product_id))
            except ValueError:
                raise ValidationError("product id must be number")
            
            quantity = self._parse_quantity(quantity)
            merged[product_id] = merged.get(product_id, 0) + quantity
        return merged


    def create(self, customer_id, items):
        if not items:
            raise ValidationError("Order must have at least one item.")

        if self.customer_repo.search_by_id(customer_id) is None:
            raise NotFoundError("Customer not found!")
        
        items = self.merge_items(items)

        total_price = Decimal("0")
        order_items = []
        for product_id, quantity in items.items():
            product = self.product_repo.search_by_product_id(product_id)

            if product is None:
                raise NotFoundError(f"Product not found: {product_id}")
            if product.is_active == 0:
                raise ValidationError(f"Product not active: {product_id}")
            if quantity > product.stock_quantity:
                raise InsufficientStockError(f"Insufficient stock for product {product_id} (requested: {quantity}).")

            order_items.append(OrderItem(
                order_item_id = None,
                order_id = None,
                product_id = product_id,
                unit_price = product.price,
                quantity = quantity,

            ))
            total_price += product.price * quantity

        order = Order(
                order_id = None,
                customer_id = customer_id,
                order_date = datetime.now(),
                total_price = total_price
        )

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            order_id = self.order_repo.create(order, cursor)
            for item in order_items:
                item.order_id = order_id
            self.item_repo.create(order_items, cursor)

            for item in sorted(order_items, key=lambda i: i.product_id):
                self.product_repo.reduce_stock(item.product_id, item.quantity, cursor)

            conn.commit()
            return order_id
        
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


            

    def get_order_by_id(self, order_id):
        order = self.order_repo.search_by_order_id(order_id)
        if order is None:
            raise NotFoundError("Order not found.")
        return order


    def get_order_by_customer_id(self, customer_id):
        customer = self.customer_repo.search_by_id(customer_id)
        if customer is None:
            raise NotFoundError("customer not found")
        
        return self.order_repo.search_by_customer_id(customer_id)
        


    def get_orders(self):
        return self.order_repo.get_all_orders()


    def get_order_items_by_id(self, order_item_id):
        order_items = self.item_repo.search_by_order_item_id(order_item_id)
        if order_items is None:
            raise NotFoundError("Order item not found.")
        return order_items


    def get_order_item_by_order_id(self, order_id):
        order = self.order_repo.search_by_order_id(order_id)
        if order is None:
            raise NotFoundError("Order not found")
        return self.item_repo.search_by_order_id(order_id)
    

    def get_order_items(self):
        return self.item_repo.get_all_order_items()


    def get_order_details(self, order_id):
        order = self.get_order_by_id(order_id)
        items = self.item_repo.search_by_order_id(order_id)
        return order, items
    


    

            
            
            
            
        
