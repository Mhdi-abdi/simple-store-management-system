from src.exceptions import AppError
from src.service.product_service import ProductService

product_service = ProductService()

def ask_id(prompt):
    while True:
        value = input(f"{prompt} (press Enter to cancel): ").strip()
        if value == "":
            return None
        if not value.isdigit():
            print("ID must be a number.")
            continue
        return int(value)


def create_product():
    product_name = input("Enter the product name: ")
    price = input("Enter the product price: ")
    stock_quantity = input("Enter the product stock quantity: ")
    description = input("Enter the product description (Optional: Press enter to skip): ")

    try:
        product_id = product_service.create(
            product_name = product_name,
            price = price,
            stock_quantity = stock_quantity,
            description = description
        )
        print(f"\nProduct created with id: {product_id}")
    except AppError as error:
        print(f"\nERROR: {error}")


def show_product(product):
    print("-" * 50)
    print(f"Product ID: {product.product_id}")
    print(f"Product Name: {product.product_name}")
    print(f"Price: {product.price}")
    print(f"stock Quantity: {product.stock_quantity}")
    print(f"description: {product.description or '-'}")
    print(f"Is Active: {product.is_active}")
    print("-" * 50)


def show_product_menu():
    while True:
        print("\n1. search by id")
        print("2. search by name")
        search = input("Please enter one choice (press Enter to cancel): ").strip()
        if search == "":
            break
        elif not search.isdigit() or int(search) not in range(1, 3)  :
            print("Please input one number between 1 to 2. ")
            continue
        elif search  == "1":
            show_product_by_id()
            break
        elif search == "2":
            show_product_by_name()
            break


def show_product_by_id():
    product_id = ask_id("Enter product id to show")
    if product_id is None:
        return
    try:
        product = product_service.get_product_by_id(product_id)
        show_product(product)
    except AppError as error:
        print(f"ERROR: {error}")


def show_product_by_name():
    name = input("Enter product name (Press Enter to cancel): ").strip()
    if name == "":
        return
    try:
        product = product_service.get_product_by_name(name)
        show_product(product)
    except AppError as error:
        print(f"ERROR: {error}")

    
def show_product_table(products):
    id_len = 5
    product_name_len = 15
    price_len = 9
    stock_len = 6
    description_len = 40
    is_active_len = 6

    if not products:
        print("Products list is empty")
        return

    line_len = (id_len + product_name_len + price_len + stock_len
                + description_len + is_active_len + 5)

    print(f"\n{'ID':<{id_len}}|{'Product name':<{product_name_len}.{product_name_len}}|{'Price':<{price_len}.{price_len}}|{'Stock':<{stock_len}}|{'Description':<{description_len}.{description_len}}|{'Active':<{is_active_len}}")
    print("-" * line_len)

    for product in products:
        product_id = str(product.product_id)
        name = product.product_name
        price = str(product.price)
        stock = str(product.stock_quantity)
        description = product.description or '-'
        active = str(product.is_active)

        print(f"{product_id:<{id_len}}|{name:<{product_name_len}.{product_name_len}}|{price:<{price_len}.{price_len}}|{stock:<{stock_len}}|{description:<{description_len}.{description_len}}|{active:<{is_active_len}}")


def show_product_description():
    product_id = ask_id("Enter product id to show description")
    if product_id is None:
        return
    try:
        description = product_service.get_description_by_id(product_id)
        if description is None:
            print("\nNo description!")
        else:
            print(description)
    except AppError as error:
        print(f"ERROR: {error}")


def update_product():
    field_dict = {1 : "product_name", 2 : "price", 3 : "description"}

    product_id = ask_id("Enter product id for update")
    if product_id is None:
        return

    print("1. Product Name")
    print("2. Price")
    print("3. Description")

    while True:
        field = input("Enter Field Number (Press Enter to cancel): ").strip()

        if field == "":
            return

        if not field.isdigit() or int(field) not in range(1, 4):
            print("\nField must be a number between 1 to 3")
            continue
        else:
            break
    field = int(field)

    new_value = input("Enter new value for update: ").strip()

    try:
        product_service.update_product(product_id, field_dict[field], new_value)
        print(f"\nProduct updated with {field_dict[field]} : {new_value}")
    except AppError as error:
        print(f"ERROR: {error}")


def active_menu():
    product_id = ask_id("Enter product id for active or deactive")
    if product_id is None:
        return
    print("\n1. Active")
    print("2. Deactive")
    choice = input("Enter your choice (Press enter to cancel): ").strip()
    
    if choice == "":
        return

    if choice not in ("1", "2"):
        print("your choice must be a number between 1 to 2")
        return

    try:
        if choice == "1":
            product_service.active_status(product_id)
            print(f"\nProduct {product_id} activate successfully")
        elif choice == "2":
            product_service.deactive_status(product_id)
            print(f"\nProduct {product_id} deactivate successfully")
    except AppError as error:
        print(f"ERROR: {error}")

        
def add_stock():
    product_id = ask_id("Enter product id to add stock")
    
    if product_id is None:
        return
    new_stock = input("Enter new stock (Press Enter to cancel): ").strip()

    if new_stock == "":
        return
    try:
        product_service.add_stock(product_id, new_stock)
        print(f"\nproduct {product_id} added stock successfully")
    except AppError as error:
        print(f"ERROR: {error}")


def product_interface():
    while True:
        print("\n1. Create product")
        print("2. See product information")
        print("3. See all products")
        print("4. See product description")
        print("5. Update product")
        print("6. Active/Deactive product")
        print("7. Add stock")
        print("8. Back")
        choice = input("\nPlease enter one choice: ").strip()
        if not choice.isdigit() or int(choice) not in range(1, 9):
            print("Your choice must be a number between 1 to 8")
            continue

        if choice == "1":
            create_product()

        elif choice == "2":
            show_product_menu()

        elif choice == "3":
            products = product_service.get_all_products()
            show_product_table(products)

        elif choice == "4":
            show_product_description()

        elif choice == "5":
            update_product()

        elif choice == "6":
            active_menu()

        elif choice == "7":
            add_stock()

        else:
            break
