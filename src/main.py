from frontend import *

def main():
    """
    CLI loop:
        - Gets menu selection
        - Collects input
        - Calls appropriate handler
        - Prints returned result
    """
    while True:
        try:
            choice = display_main_menu()

            if choice == 1:
                name = input("Enter account holder name: ")
                balance = float(input("Enter initial deposit: "))
                print(handle_create_account(name, balance))

            elif choice == 2:
                acc_id = input("Enter account ID: ")
                amount = float(input("Enter deposit amount: "))
                print(handle_deposit(acc_id, amount))

            elif choice == 3:
                acc_id = input("Enter account ID: ")
                amount = float(input("Enter withdrawal amount: "))
                print(handle_withdraw(acc_id, amount))

            elif choice == 4:
                src = input("Enter source account ID: ")
                dest = input("Enter destination account ID: ")
                amount = float(input("Enter transfer amount: "))
                print(handle_transfer(src, dest, amount))

            elif choice == 5:
                acc_id = input("Enter account ID: ")
                print(handle_view_account(acc_id))

            elif choice == 6:
                print(handle_list_accounts())

            elif choice == 7:
                print("Exiting program.")
                break

            else:
                print("Invalid selection.")

        except ValueError:
            print("Invalid input. Please enter correct data types.")


if __name__ == "__main__":
    main()