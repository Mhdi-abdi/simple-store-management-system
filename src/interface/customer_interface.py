from src.exceptions import AppError
from src.service.customer_service import CustomerService

customer_service = CustomerService()

def ask_id(prompt):
    while True:
        value = input(f"{prompt} (press Enter to cancel): ").strip()
        if value == "":
            return None
        if not value.isdigit():
            print("ID must be a number.")
            continue
        return int(value)
    

def create_customer():
    first_name = input("Enter the customer first name: ")
    last_name = input("Enter the customer last name: ")
    email = input("Enter the customer email: ")
    phone = input("Enter the customer Phone number (Optional: Press enter to skip): ")
    city = input("Enter the customer city (Optional: Press enter to skip): ")
    country = input("Enter the customer country (Optional: Press enter to skip): ")
    postal_code = input("Enter the customer postal code (Optional: Press enter to skip): ")
    
    try:
        customer_id = customer_service.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            city = city,
            country = country,
            postal_code = postal_code
        )
        print(f"\nCustomer created with id: {customer_id}")
    except AppError as error:
        print(f"\nERROR: {error}")


def show_customer(customer):
    print("-" * 50)
    print(f"Customer ID: {customer.customer_id}")
    print(f"First Name: {customer.first_name}")
    print(f"Last Name: {customer.last_name}")
    print(f"Email: {customer.email}")
    print(f"Phone: {customer.phone or '-'}")
    print(f"City: {customer.city or '-'}")
    print(f"Country: {customer.country or '-'}")
    print(f"Postal Code: {customer.postal_code or '-'}")
    print("-" * 50)


def show_customer_menu():
    while True:
        print("\n1. search by id")
        print("2. search by email")
        search = input("Please enter one choice (press Enter to cancel): ").strip()
        if search == "":
            break
        elif not search.isdigit() or int(search) not in range(1, 3)  :
            print("Please input one number between 1 to 2. ")
            continue
        elif search  == "1":
            show_customer_by_id()
            break
        elif search == "2":
            show_customer_by_email()
            break


def show_customer_by_id():
    customer_id = ask_id("Enter customer id to show")
    if customer_id is None:
        return
    try:
        customer = customer_service.get_customer_by_id(customer_id)
        show_customer(customer)
    except AppError as error:
        print(f"ERROR: {error}")


def show_customer_by_email():
    email = input("Enter customer email (Press Enter to cancel): ").strip()
    if email == "":
        return
    
    try:
        customer = customer_service.get_customer_by_email(email)
        show_customer(customer)
    except AppError as error:
        print(f"ERROR: {error}")


def show_customers_table(customers):
    id_len = 5
    first_name_len = last_name_len = 11
    email_len = 40
    if not customers:
        print("Customers list is empty")
        return
    
    print(f"\n{'ID':<{id_len}}|{'First Name':<{first_name_len}.{first_name_len}}|{'Last Name':<{last_name_len}.{last_name_len}}|{'EMAIL':<{email_len}.{email_len}}")
    print("-" * 70)
    for customer in customers:
        print(f"{str(customer.customer_id):<{id_len}}|{customer.first_name:<{first_name_len}.{first_name_len}}|{customer.last_name:<{last_name_len}.{last_name_len}}|{customer.email:<{email_len}.{email_len}}")


def update_customer():
    field_dict = {1 : "first_name", 2 : "last_name", 3 : "email", 4 : "phone", 5 : "city", 6 : "country", 7 : "postal_code" }

    customer_id = ask_id("Enter customer id for update")
    if customer_id is None:
        return

    print("1. First Name")
    print("2. Last Name")
    print("3. Email")
    print("4. Phone")
    print("5. City")
    print("6. Country")
    print("7. Postal Code")

    while True:
        field = input("Enter Field Number (Press Enter to cancel): ").strip()

        if field == "":
            return

        if not field.isdigit() or int(field) not in range(1, 8):
            print("Field must be a number between 1 to 7")
            continue
        else:
            break
    field = int(field)

    new_value = input("Enter new value for update: ").strip()

    try:
        customer_service.update_customer(customer_id, field_dict[field], new_value)
        print(f"Customer updated with {field_dict[field]} : {new_value}")
    except AppError as error:
        print(f"ERROR: {error}")


def delete_customer():
    customer_id = ask_id("Enter customer id for delete")
    if customer_id is None:
        return

    trust = input(f"Do You want delete customer: {customer_id} --> yes/no: ").strip()
    if trust.lower() == "yes":
        try:
            customer_service.delete_customer(customer_id)
            print(f"Customer deleted with ID: {customer_id}")
        except AppError as error:
            print(f"ERROR: {error}")
    else:
        return
        

def customer_interface():
    while True:
        print("\n1. Create customer")
        print("2. See customer information")
        print("3. See all customers")
        print("4. Update customer")
        print("5. Delete customer")
        print("6. Back")

        choice = input("\nPlease enter one choice: ").strip()
        if not choice.isdigit() or int(choice) not in range(1, 7):
            print("Your choice must be a number between 1 to 6")
            continue

        if choice == "1":
            create_customer()

        elif choice == "2":
            show_customer_menu()

        elif choice == "3":
            customers = customer_service.get_all_customer()
            show_customers_table(customers)

        elif choice == "4":
            update_customer()

        elif choice == "5":
            delete_customer()
            
        elif choice == "6":
            break

