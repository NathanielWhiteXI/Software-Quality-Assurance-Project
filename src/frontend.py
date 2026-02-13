# Later: Create a Backend module called controller

# SESSION STATE

current_session = {
    "logged_in": False,
    "mode": None,          # "standard" or "admin"
    "account_holder": None # Only used in standard mode
}

# Track total paid per company in session (standard mode restriction)
session_bill_totals = {
    "EC": 0.0,
    "CQ": 0.0,
    "FI": 0.0
}

VALID_COMPANIES = {
    "EC": "The Bright Light Electric Company (EC)",
    "CQ": "Credit Card Company Q (CQ)",
    "FI": "Fast Internet, Inc. (FI)"
}

# MAIN MENU

def display_main_menu():
    print("\n<+= Banking System =+>")
    print("1. Login")
    print("2. Logout")
    print("3. Create Account")
    print("4. Deposit")
    print("5. Withdraw")
    print("6. Transfer")
    print("7. Pay Bill")
    print("8. View Account")
    print("9. List All Accounts")
    print("10. Exit")

    choice = input("Select an option: ")
    return int(choice)

# LOGIN

def handle_login(session_type: str, account_holder: str | None = None):
    """
    Returns: Success and/or error message (str)
    """
    global current_session

    if current_session["logged_in"]:
        return "Error: Already logged in. Please logout first."

    if session_type not in ["standard", "admin"]:
        return "Error: Invalid session type."

    if session_type == "standard" and not account_holder:
        return "Error: Standard login requires account holder name."

    # controller.load_accounts_file()  # backend responsibility

    current_session["logged_in"] = True
    current_session["mode"] = session_type
    current_session["account_holder"] = account_holder

    return f"Login successful ({session_type} mode)."


# LOGOUT

def handle_logout() -> str:
    global current_session, session_bill_totals

    if not current_session["logged_in"]:
        return "Error: No active session."

    # controller.save_transactions()  # backend responsibility

    current_session = {
        "logged_in": False,
        "mode": None,
        "account_holder": None
    }

    # Reset session bill totals
    session_bill_totals = { "EC": 0.0, "CQ": 0.0, "FI": 0.0 }

    return "Logout successful."



# ACCOUNT CREATION

def handle_create_account(name: str, initial_balance: float):
    """
    Returns: Success or error message (str)

    Expected backend call:
        controller.create_account(name, initial_balance)
    """
    try:
        # account = controller.create_account(name, initial_balance)
        return f"Account successfully created for {name}."
    except Exception as e:
        return f"Error creating account: {str(e)}"


# DEPOSIT

def handle_deposit(account_id: str, amount: float):
    """
    Returns: Success or error message (str)
    """
    try:
        # controller.deposit(account_id, amount)
        return "Deposit successful."
    except Exception as e:
        return f"Deposit failed: {str(e)}"


# WITHDRAW

def handle_withdraw(account_id: str, amount: float):
    """
    Returns: Success or error message (str)
    """
    try:
        # controller.withdraw(account_id, amount)
        return "Withdrawal successful."
    except Exception as e:
        return f"Withdrawal failed: {str(e)}"


# TRANSFER FUNDS

def handle_transfer(src_id: str, dest_id: str, amount: float):
    """
    Returns: Success or error message (str)
    """
    try:
        # controller.transfer(src_id, dest_id, amount)
        return "Transfer successful."
    except Exception as e:
        return f"Transfer failed: {str(e)}"

# PAY BILL

def handle_paybill(account_number: str, company_code: str, amount: float, account_holder: str | None = None):
    """
    Constraints:
        - Must be logged in
        - Standard mode: only own account
        - Company must be EC, CQ, or FI
        - Max $2000 per company per session in standard mode
        - Balance must remain >= 0
    """
    global session_bill_totals

    if not current_session["logged_in"]:
        return "Error: You must login first."

    if company_code not in VALID_COMPANIES:
        return "Error: Invalid company."

    if amount <= 0:
        return "Error: Invalid payment amount."

    # If admin, require account holder name
    if current_session["mode"] == "admin":
        if not account_holder:
            return "Error: Admin must specify account holder name."
    else:
        # Standard mode
        account_holder = current_session["account_holder"]

        # Enforcement: $2000 per company
        if session_bill_totals[company_code] + amount > 2000.00:
            return "Error: Exceeds $2000 session limit for this company."

    try:
        # Backend validation:
        # - Check account exists
        # - Check belongs to account_holder
        # - Check balance >= 0 after withdrawal
        # controller.pay_bill(account_holder, account_number, company_code, amount)

        # Update session total (for standard)
        if current_session["mode"] == "standard":
            session_bill_totals[company_code] += amount

        return f"Bill paid successfully to {VALID_COMPANIES[company_code]}."

    except Exception as e:
        return f"Paybill failed: {str(e)}"


# PROTECTED ACTION CHECK

def require_login():
    """
    Utility function: Ensures user is logged in before any transaction.
    """
    if not current_session["logged_in"]:
        print("Error: You must login first.")
        return False
    return True


# VIEW ACCOUNT

def handle_view_account(account_id: str):
    """
    Returns: Account details (object) or error message (str)
    """
    try:
        # account = controller.get_account(account_id)
        # return str(account)
        return f"Displaying account details for ID {account_id}"
    except Exception as e:
        return f"Error retrieving account: {str(e)}"


# LIST ALL ACCOUNTS

def handle_list_accounts():
    """
    Returns: List of accounts (list) or error message (str)
    """
    try:
        # accounts = controller.get_all_accounts()
        # return accounts
        return "Listing all accounts..."
    except Exception as e:
        return f"Error listing accounts: {str(e)}"
