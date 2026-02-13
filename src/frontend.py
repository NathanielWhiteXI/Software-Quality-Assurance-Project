# Later: Create a Backend module called controller

# -----------------------------
# MAIN MENU
# -----------------------------

def display_main_menu():
    print("\n=== Banking System ===")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. View Account")
    print("6. List All Accounts")
    print("7. Exit")

    choice = input("Select an option: ")
    return int(choice)


# -----------------------------
# ACCOUNT CREATION
# -----------------------------

def handle_create_account(name: str, initial_balance: float):
    """
    Creates an account.

    Returns:
        str: Success or error message

    Expected backend call:
        controller.create_account(name, initial_balance)
    """
    try:
        # account = controller.create_account(name, initial_balance)
        return f"Account successfully created for {name}."
    except Exception as e:
        return f"Error creating account: {str(e)}"


# -----------------------------
# DEPOSIT
# -----------------------------

def handle_deposit(account_id: str, amount: float):
    """
    Deposits money into an account.

    Returns:
        str: Success or error message
    """
    try:
        # controller.deposit(account_id, amount)
        return "Deposit successful."
    except Exception as e:
        return f"Deposit failed: {str(e)}"


# -----------------------------
# WITHDRAW
# -----------------------------

def handle_withdraw(account_id: str, amount: float):
    """
    Withdraws money from an account.

    Returns:
        str: Success or error message
    """
    try:
        # controller.withdraw(account_id, amount)
        return "Withdrawal successful."
    except Exception as e:
        return f"Withdrawal failed: {str(e)}"


# -----------------------------
# TRANSFER
# -----------------------------

def handle_transfer(src_id: str, dest_id: str, amount: float):
    """
    Transfers funds between accounts.

    Returns:
        str: Success or error message
    """
    try:
        # controller.transfer(src_id, dest_id, amount)
        return "Transfer successful."
    except Exception as e:
        return f"Transfer failed: {str(e)}"


# -----------------------------
# VIEW ACCOUNT
# -----------------------------

def handle_view_account(account_id: str):
    """
    Retrieves account details.

    Returns:
        str or object: Account details or error message
    """
    try:
        # account = controller.get_account(account_id)
        # return str(account)
        return f"Displaying account details for ID {account_id}"
    except Exception as e:
        return f"Error retrieving account: {str(e)}"


# -----------------------------
# LIST ALL ACCOUNTS
# -----------------------------

def handle_list_accounts():
    """
    Retrieves all accounts.

    Returns:
        list or str: List of accounts or error message
    """
    try:
        # accounts = controller.get_all_accounts()
        # return accounts
        return "Listing all accounts..."
    except Exception as e:
        return f"Error listing accounts: {str(e)}"
