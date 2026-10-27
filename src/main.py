import mysql.connector

from src.interface.customer_interface import customer_interface
from src.interface.product_interface import product_interface
from src.interface.order_interface import order_interface


def main():
    print("\n--Welcome to my store--")
    try:
        while True:
            print("\n1. Customer")
            print("2. Product")
            print("3. Order")
            print("4. Quit")
            choice = input("\nPlease enter one choice (Press Enter to quit): ").strip()

            if choice in ("", "4"):
                break

            try:
                if choice == "1":
                    customer_interface()
                elif choice == "2":
                    product_interface()
                elif choice == "3":
                    order_interface()
                else:
                    print("\nYour choice must be a number between 1 and 4")
            except mysql.connector.Error as error:
                print("\nA database error occurred. Please check the connection and try again.")
                print(f"Details: {error}")  # only for development, remove later

    except KeyboardInterrupt:
        print()

    print("\nGoodbye!")


if __name__ == "__main__":
    main()