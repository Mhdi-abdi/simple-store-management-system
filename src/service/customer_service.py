from src.exceptions import ValidationError, NotFoundError, DuplicateError
from src.model.customer import Customer
from src.repository.customer_repository import CustomerRepository
from src.repository.order_repository import OrderRepository


class CustomerService:

    FIELD_RULES = {
        "first_name" : (True, 50),
        "last_name" : (True, 50),
        "email" : (True, 255),
        "phone" : (False, 11),
        "city" : (False, 45),
        "country" : (False, 45),
        "postal_code" : (False, 45)
    }


    def __init__(self):
        self.customer_repo = CustomerRepository()
        self.order_repo =OrderRepository()


    @classmethod
    def _validate_field(cls, field, value):
        if field not in cls.FIELD_RULES:
            raise ValidationError(f"invalid field: {field}.")

        required, max_len = cls.FIELD_RULES[field]

        if value is not None:
            value = str(value).strip()

        if not value:
            if required:
                raise ValidationError(f"{field} is required.")
            return None

        if len(value) > max_len:
            raise ValidationError(f"{field} can not be longer than {max_len} characters.")

        if field in ["first_name", "last_name", "city", "country"]:
            for part in value.split(" "):
                if not part.isalpha():
                    raise ValidationError(f"{field} must contain letters only.")

        if field == "email":
            value = value.lower()
            if " " in value or value.count("@") != 1 :
                raise ValidationError("Email format is invalid.")

            local, domain = value.split("@")
            if not local or not domain:
                raise ValidationError("Email format is invalid.")

        if field == "phone" and not value.isdigit():
            raise ValidationError("Phone must contain digits only.")

        if field == "postal_code":
            for part in value.split("-"):
                if not part.isdigit():
                    raise ValidationError(f"{field} must contain numbers only.")
        return value


    def _check_email_is_free(self, email, ignore_customer_id = None):
        existing = self.customer_repo.search_by_email(email)
        if existing and existing.customer_id != ignore_customer_id :
            raise DuplicateError("A customer with this email already exist.")


    def create(self, first_name, last_name, email, phone = None, city = None, country = None, postal_code = None):
        
        first_name = self._validate_field("first_name", first_name)
        last_name = self._validate_field("last_name", last_name)
        email = self._validate_field("email", email)
        phone = self._validate_field("phone", phone)
        city = self._validate_field("city", city)
        country = self._validate_field("country", country)
        postal_code = self._validate_field("postal_code", postal_code)

        self._check_email_is_free(email)

        customer = Customer(
            customer_id = None,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            city = city,
            country = country,
            postal_code = postal_code
        )

        return self.customer_repo.create(customer)


    def get_customer_by_id(self, customer_id):
        customer = self.customer_repo.search_by_id(customer_id)
        if customer is None:
            raise NotFoundError("Customer not found.")
        return customer

    def get_customer_by_email(self, email):
        email = self._validate_field("email", email)
        customer = self.customer_repo.search_by_email(email)
        if customer is None:
            raise NotFoundError("Customer not found.")
        return customer
    

    def get_all_customer(self):
        return self.customer_repo.get_all_customers()
    

    def update_customer(self, customer_id, field, new_value):
        self.get_customer_by_id(customer_id)

        new_value = self._validate_field(field, new_value)

        if field == "email":
            self._check_email_is_free(new_value, ignore_customer_id = customer_id)

        self.customer_repo.update_customer(customer_id, field, new_value)


    def delete_customer(self, customer_id):
        self.get_customer_by_id(customer_id)
        order = self.order_repo.search_by_customer_id(customer_id)

        if order:
            raise ValidationError("This customer has orders and can not be deleted.")
        
        self.customer_repo.delete_customer(customer_id)

        
