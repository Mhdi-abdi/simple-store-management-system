from src.interface.customer_interface import customer_interface
from src.interface.product_interface import product_interface
from src.interface.order_interface import order_interface

def main():
    print("\n--Welcome to my srore--")
    while True:
        print("1. Customer")
        print("2. Product")
        print("3. Order")
        print("4. Quit")
        choice = input("\nPlease Enter one choice (Press Enter to cancel): ").strip()

        if choice == "":
            print("GoodBye!")
            break

        if not choice.isdigit() or int(choice) not in range(1, 5):
            print("\nYour choice must be a number 1 to 4")
            continue

        elif choice == "1":
            customer_interface()

        elif choice == "2":
            product_interface()

        elif choice == "3":
            order_interface()

        else:
            print("\ngoodBye!")
            break


if __name__ == "__main__":
    main()