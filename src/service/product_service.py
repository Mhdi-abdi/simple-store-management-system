from decimal import Decimal, InvalidOperation

from src.exceptions import ValidationError, NotFoundError, DuplicateError
from src.model.product import Product
from src.repository.product_repository import ProductRepository

class ProductService:

    TEXT_RULES = {
        "product_name" : (True, 255),
        "description" : (False, 255)
    }

    max_quantity = 2147483647
    max_price = Decimal("9999999.99")
    UPDATABLE_FIELDS = ("product_name", "price", "description")

    def __init__(self):
        self.product_repo = ProductRepository()

    @classmethod
    def _parse_int(cls, value, name):
        try:
            number = int(str(value).strip())
        except ValueError:
            raise ValidationError(f"{name} must be whole number.")
        if number > cls.max_quantity:
            raise ValidationError(f"{name} is too large.")

        return number

    @classmethod
    def _parse_price(cls, value):
        try:
            price = Decimal(str(value).strip())
        except InvalidOperation:
            raise ValidationError("price must be a number.")
        if not price.is_finite():
            raise ValidationError("price must be a number")
        if price <= 0:
            raise ValidationError("price must be greater than zero.")
        if price.as_tuple().exponent < -2:
            raise ValidationError("price can have at most 2 decimal places.")
        if price > cls.max_price:
            raise ValidationError("price is too large")
        return price

    @classmethod
    def _validate_field(cls, field, value):
        if field == "price":
            return cls._parse_price(value)


        if field == "stock_quantity":
            stock = cls._parse_int(value, "stock quantity")
            if stock < 0:
                raise ValidationError("stock quantity must be zero or greater than zero.")
            return stock
        
        if field not in cls.TEXT_RULES:
            raise ValidationError(f"invalid field: {field}")

        required, max_len = cls.TEXT_RULES[field]

        if value is not None:
            value = str(value).strip()

        if not value:
            if required :
                raise ValidationError(f"{field} is required.")
            return None


        if len(value) > max_len:
            raise ValidationError(f"{field} can not be longer than {max_len} characters.")
        
        return value


    def _check_name_is_free(self, name, ignore_product_id = None):
        existing = self.product_repo.search_by_name(name)
        if existing and existing.product_id != ignore_product_id:
            raise DuplicateError("this product name already exist.")
        

    def create(self, product_name, price, stock_quantity, description = None):
        product_name = self._validate_field("product_name", product_name)
        price = self._validate_field("price", price)
        stock_quantity = self._validate_field("stock_quantity", stock_quantity)
        description = self._validate_field("description", description)

        self._check_name_is_free(product_name)

        product = Product(
            product_id = None,
            product_name = product_name,
            price = price,
            stock_quantity = stock_quantity,
            description = description,
            is_active = True
        )

        return self.product_repo.create(product)
    

    def get_product_by_id(self, product_id):
        product = self.product_repo.search_by_product_id(product_id)
        if product is None:
            raise NotFoundError("product not found.")
        return product
    

    def get_product_by_name(self, name):
        name = self._validate_field("product_name", name)
        product = self.product_repo.search_by_name(name)
        if product is None:
            raise NotFoundError("product not found.")
        return product
    

    def get_all_products(self):
        return self.product_repo.get_all_products()
    

    def get_description_by_id(self, product_id):
        self.get_product_by_id(product_id)
        return self.product_repo.get_product_description(product_id)


    def update_product(self, product_id, field, new_value):
        if field not in self.UPDATABLE_FIELDS:
            raise ValidationError("this field not allowed for update.")
        
        self.get_product_by_id(product_id)

        new_value = self._validate_field(field, new_value)

        if field == "product_name":
            self._check_name_is_free(new_value, ignore_product_id = product_id)

        self.product_repo.update_product(product_id, field, new_value)


    def add_stock(self, product_id, new_stock):
        self.get_product_by_id(product_id)
        new_stock = self._validate_field("stock_quantity", new_stock)
        if new_stock <= 0:
            raise ValidationError("new stock quantity must be greater than zero")
        self.product_repo.increase_stock(product_id, new_stock)


    def active_status(self, product_id):
        self.get_product_by_id(product_id)
        self.product_repo.toggle_product_status(product_id, 1)


    def deactive_status(self, product_id):
        self.get_product_by_id(product_id)
        self.product_repo.toggle_product_status(product_id, 0)

