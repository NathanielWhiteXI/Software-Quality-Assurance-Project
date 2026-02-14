from frontend import *
'''
NOTE: You must run this from the terminal for the program to work correctly. This is a controller for the entire program. In its current iteration, 
it only supports frontend functionality.

This uses an if/else statement to control which selection goes to which mode.

More information pertaining to how the front-end works can be found there.
'''


def main():
    while True:
            #Runs the front-end loop.
            choice, front_end_mode = display_main_menu()

            # LOGIN: Logs in the person.
            if choice == 1:
                session_type = input("Enter session type (standard/admin): ").lower()

                #Handles the proper log-in procedure.
                if session_type == "standard":
                    name = input("Enter account holder name: ")
                    print(handle_login(session_type, name))

                elif session_type == "admin":
                    print(handle_login(session_type))

                else:
                    print("Invalid session type.")

            # LOGOUT: Logs out the person
            elif choice == 2 and front_end_mode in ["b", "c"]:
                print(handle_logout())

            # CREATE ACCOUNT: Creates a bank account, currently partially implemented.
            elif choice == 3 and front_end_mode in ["b", "c"]:
                if not require_login():
                    continue

                name = input("Enter account holder name: ")
                balance = float(input("Enter initial deposit: "))
                print(handle_create_account(name, balance))

            # DEPOSIT: Deposits to a bank account, currently deposits to a fictious account.
            elif choice == 4 and front_end_mode in ["b", "c"]:
                if not require_login():
                    continue

                acc_id = input("Enter account ID: ")
                amount = float(input("Enter deposit amount: "))
                print(handle_deposit(acc_id, amount))

            # WITHDRAW: Withdraws from a bank account, currently deposits to a fictious account.
            elif choice == 5 and front_end_mode in ["b", "c"]:
                if not require_login():
                    continue

                acc_id = input("Enter account ID: ")
                amount = float(input("Enter withdrawal amount: "))
                print(handle_withdraw(acc_id, amount))

            # TRANSFER: Transfers an amount of money between bank accounts.
            elif choice == 6 and front_end_mode in ["b", "c"]:
                if not require_login():
                    continue

                src = input("Enter source account ID: ")
                dest = input("Enter destination account ID: ")
                amount = float(input("Enter transfer amount: "))
                print(handle_transfer(src, dest, amount))

            # PAY BILL: Pays a bill to one of 3 approve payees.
            elif choice == 7 and front_end_mode in ["b", "c"]:
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

            # VIEW ACCOUNT: Displays account information given an account handle.
            elif choice == 8 and front_end_mode in ["b", "c"]:
                if not require_login():
                    continue

                acc_id = input("Enter account ID: ")
                print(handle_view_account(acc_id))

            # LIST ALL ACCOUNTS: Lists all accounts under a given name.
            elif choice == 9 and front_end_mode in ["b", "c"]:
                if not require_login():
                    continue

                print(handle_list_accounts())

            # DELETE: Deletes an account (Admin only)
            elif choice == 10 and front_end_mode == "c":
                holder = input("Enter account holder name: ")
                acc_number = input("Enter account number: ")
                print(handle_delete_account(holder, acc_number))

            # DISABLE: Disables an account (Admin only)
            elif choice == 11 and front_end_mode == "c":
                holder = input("Enter account holder name: ")
                acc_number = input("Enter account number: ")
                print(handle_disable_account(holder, acc_number))

            # CHANGE PLAN: Changes the plan on an account (Admin Only)
            elif choice == 12 and front_end_mode == "c":
                holder = input("Enter account holder name: ")
                acc_number = input("Enter account number: ")
                print(handle_change_plan(holder, acc_number))

            # EXIT: Exits the program
            elif (choice == 13 and front_end_mode == "c") or (choice == 10 and front_end_mode == "b") or (choice == 2 and front_end_mode == "a"):
                print("Exiting program.")
                break

            # Case if the person does not enter a valid selection.
            else:
                print("Invalid selection.")


if __name__ == "__main__":
    main()
