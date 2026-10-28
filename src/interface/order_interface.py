from src.exceptions import AppError
from src.service.order_service import OrderService
from src.service.product_service import ProductService
from src.service.customer_service import CustomerService
from src.interface.product_interface import show_product_table
from src.interface.helpers import ask_id

order_service= OrderService()
product_service = ProductService()
customer_service = CustomerService()


def ask_quantity():
    while True:
        quantity = input("Enter the quantity you want(Press Enter to cancel): ").strip()
        if quantity == "":
            break
        if not quantity.isdigit():
            print("Quantity must be a number.")
            continue
        if int(quantity) <= 0:
            print("quantity must be a number greater than 0")
            continue
        return int(quantity)


def create_order():
    customer_id = ask_id("Enter customer id for order")
    if customer_id is None:
        return
    try:
        customer = customer_service.get_customer_by_id(customer_id)
    except AppError as error:
        print(f"ERROR: {error}")
        return
    
    product_list = {}
    while True:
        products = product_service.get_all_products()
        show_product_table(products)

        product_id = ask_id("Enter product id to order")
        if product_id is None :
            break
        try:
            product = product_service.get_product_by_id(product_id)
        except AppError as error:
            print(f"ERROR: {error}")
            continue

        if not product.is_active:
            print("Product Not Active")
            continue

        quantity = ask_quantity()
        if quantity is None:
            break

        if product_id in product_list:
            product_list[product_id] += quantity
        else:
            product_list[product_id] = quantity

        print("\n1. Add another product")
        print("2. Review order")
        request = input("\nEnter your choice (1 to add more, anything else to review the order): ").strip()
        if request == "1": 
            continue 
        else:
            break

    try:
        if not product_list:
            print("\nOrder cancelled")
            return
        
        all_price = 0
        print(f"\nCustomer ID: {customer_id}|Customer Name = {customer.first_name + ' ' + customer.last_name}")

        items = []
        for id, quantity in product_list.items():
            items.append([id, quantity])
            every_product = product_service.get_product_by_id(id)
            all_price += every_product.price * quantity
            print(f"\nProduct ID: {id}|Product Name: {every_product.product_name}|Quantity: {quantity}|Price: {every_product.price}")
        print(f"Total Price: {all_price}")

        while True:
            print("\n1. Accept Order list")
            print("2. Cancel order")
            choice = input("\nPlease Enter one choice between(1, 2) (Press Enter to cancel all orders): ")
            
            if choice == "":
                print("\nOrder Cancelled")
                return
            if not choice.isdigit():
                print("\nPlease enter a number between 1 to 2")
                continue
            elif choice == "1":
                order_id = order_service.create(customer_id, items)
                print(f"\nOrder created successfully with ID: {order_id}")
                return
            elif choice == "2":
                print("\nOrder Cancelled")
                return           
            else:
                print("\nEnter number between 1 to 2 or Press Enter to cancel")
                continue
    except AppError as error:
        print(f"ERROR: {error}")


def show_order(order):
    print("-" * 50)
    print(f"Order ID: {order.order_id}")
    print(f"Customer ID: {order.customer_id}")
    print(f"Order Date: {order.order_date}")
    print(f"Total Price: {order.total_price}")
    print("-" * 50)


def show_order_item(order_item):
    print("-" * 50)
    print(f"Order Item ID: {order_item.order_item_id}")
    print(f"Order ID: {order_item.order_id}")
    print(f"Product ID: {order_item.product_id}")
    print(f"Unit Price: {order_item.unit_price}")
    print(f"Quantity: {order_item.quantity}")
    print("-" * 50)

def show_order_menu():
    while True:
        print("\n1. search by order id")
        print("2. search by customer id")
        search = input("Please enter one choice (press Enter to cancel): ").strip()
        if search == "":
            break
        elif not search.isdigit() or int(search) not in range(1, 3)  :
            print("Please input one number between 1 to 2. ")
            continue
        elif search  == "1":
            show_order_by_id()
            break
        elif search == "2":
            show_order_by_customer_id()
            break


def show_order_by_id():
    order_id = ask_id("Enter order id to show")
    if order_id is None:
        return
    try:
        order = order_service.get_order_by_id(order_id)
        show_order(order)
    except AppError as error:
        print(f"ERROR: {error}")


def show_order_by_customer_id():
    customer_id = ask_id("Enter customer id to show")
    if customer_id is None:
        return
    try:
        orders = order_service.get_order_by_customer_id(customer_id)
        show_orders_table(orders)
    except AppError as error:
        print(f"ERROR: {error}")


def show_orders_table(orders):
    order_id_len = 8
    customer_id_len = 11
    date_len = 20
    price_len = 9

    if not orders:
        print("Order list is empty")
        return

    line_len = (order_id_len + customer_id_len + date_len + price_len+ 5)

    print(f"\n{'Order ID':<{order_id_len}}|{'Customer ID':<{customer_id_len}}|{'DATE':<{date_len}}|{'Price':<{price_len}}")
    print("-" * line_len)

    for order in orders:
        order_id = str(order.order_id)
        customer_id = str(order.customer_id)
        date = str(order.order_date)
        price = str(order.total_price)

        print(f"{order_id:<{order_id_len}}|{customer_id:<{customer_id_len}}|{date:<{date_len}}|{price:<{price_len}}")


def show_order_item_menu():
    while True:
        print("\n1. search by order item id")
        print("2. search by order id")
        search = input("Please enter one choice (press Enter to cancel): ").strip()
        if search == "":
            break
        elif not search.isdigit() or int(search) not in range(1, 3)  :
            print("Please input one number between 1 to 2. ")
            continue
        elif search  == "1":
            show_order_item_by_id()
            break
        elif search == "2":
            show_order_item_by_order_id()
            break


def show_order_item_by_id():
    order_item_id = ask_id("Enter order item id to show")
    if order_item_id is None:
        return
    try:
        order_item = order_service.get_order_items_by_id(order_item_id)
        show_order_item(order_item)
    except AppError as error:
        print(f"ERROR: {error}")


def show_order_item_by_order_id():
    order_id = ask_id("Enter order id to show")
    if order_id is None:
        return
    try:
        order_items = order_service.get_order_item_by_order_id(order_id)
        show_order_items_table(order_items)
    except AppError as error:
        print(f"ERROR: {error}")


def show_order_items_table(order_items):
    order_item_id_len = 8
    order_id_len = 8
    product_len = 11
    price_len = 10
    quantity_len = 8

    if not order_items:
        print("Order items list is empty")
        return

    line_len = (order_item_id_len + order_id_len + product_len + price_len + quantity_len + 5)


    print(f"\n{'Item ID':<{order_item_id_len}}|{'Order ID':<{order_id_len}}|{'Product ID':<{product_len}}|{'Unit Price':<{price_len}}|{'Quantity':<{quantity_len}}")
    print("-" * line_len)

    for order in order_items:
        order_item_id = str(order.order_item_id)
        order_id = str(order.order_id)
        product_id = str(order.product_id)
        unit_price = str(order.unit_price)
        quantity = str(order.quantity)

        print(f"{order_item_id:<{order_item_id_len}}|{order_id:<{order_id_len}}|{product_id:<{product_len}}|{unit_price:<{price_len}}|{quantity:<{quantity_len}}")

def show_order_details():
    order_id = ask_id("Enter order id for show details order and order items")
    if order_id is None:
        return

    try:
        order, items = order_service.get_order_details(order_id)
        show_order(order)
        show_order_items_table(items)
    except AppError as error:
        print(f"ERROR: {error}")
    

    
def order_interface():
    while True:
        print("\n1. Create Order")
        print("2. See order information")
        print("3. See all orders")
        print("4. See order item information")
        print("5. See all order items")
        print("6. See order details(order and order items)")
        print("7. Back")
        choice = input("Please Enter one choice: ").strip()
        if not choice.isdigit() or int(choice) not in range(1, 8):
            print("Your choice must be a number between 1 to 7")
            continue

        elif choice == "1":
            create_order()

        elif choice == "2":
            show_order_menu()

        elif choice == "3":
            try:
                orders = order_service.get_orders()
                show_orders_table(orders)
            except AppError as error:
                print(f"ERROR: {error}")
        elif choice == "4":
            show_order_item_menu()

        elif choice == "5":
            try:
                order_items = order_service.get_order_items()
                show_order_items_table(order_items)
            except AppError as error:
                print(f"ERROR: {error}")

        elif choice == "6":
            show_order_details()

        else:
            break

