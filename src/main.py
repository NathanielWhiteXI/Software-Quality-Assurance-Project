from frontend import *

def main():
    while True:
        try:
            choice = display_main_menu()

            # LOGIN
            if choice == 1:
                session_type = input("Enter session type (standard/admin): ").lower()

                if session_type == "standard":
                    name = input("Enter account holder name: ")
                    print(handle_login(session_type, name))
                elif session_type == "admin":
                    print(handle_login(session_type))
                else:
                    print("Invalid session type.")

            # LOGOUT
            elif choice == 2:
                print(handle_logout())

            # CREATE ACCOUNT
            elif choice == 3:
                if not require_login():
                    continue

                name = input("Enter account holder name: ")
                balance = float(input("Enter initial deposit: "))
                print(handle_create_account(name, balance))

            # DEPOSIT
            elif choice == 4:
                if not require_login():
                    continue

                acc_id = input("Enter account ID: ")
                amount = float(input("Enter deposit amount: "))
                print(handle_deposit(acc_id, amount))

            # WITHDRAW
            elif choice == 5:
                if not require_login():
                    continue

                acc_id = input("Enter account ID: ")
                amount = float(input("Enter withdrawal amount: "))
                print(handle_withdraw(acc_id, amount))

            # TRANSFER
            elif choice == 6:
                if not require_login():
                    continue

                src = input("Enter source account ID: ")
                dest = input("Enter destination account ID: ")
                amount = float(input("Enter transfer amount: "))
                print(handle_transfer(src, dest, amount))

            # PAY BILL
            elif choice == 7:
                if not require_login():
                    continue

                if current_session["mode"] == "admin":
                    holder = input("Enter account holder name: ")
                else:
                    holder = None

                acc_number = input("Enter account number: ")
                company = input("Enter company code (EC, CQ, FI): ").upper()
                amount = float(input("Enter payment amount: "))

                print(handle_paybill(acc_number, company, amount, holder))

            # VIEW ACCOUNT
            elif choice == 8:
                if not require_login():
                    continue

                acc_id = input("Enter account ID: ")
                print(handle_view_account(acc_id))

            # LIST ALL ACCOUNTS
            elif choice == 9:
                if not require_login():
                    continue

                print(handle_list_accounts())

            # EXIT PROGRAM
            elif choice == 10:
                print("Exiting program.")
                break

            else:
                print("Invalid selection.")

        except ValueError:
            print("Invalid input. Please enter correct data types.")


if __name__ == "__main__":
    main()
