# Later: Create a Backend module called controller

'''
The frontend is controlled by several dictionaries.

current_session controls the information about the front-end and its session state. It is used to show the proper front-end for the current security mode
(not logged in, standard, admin)

The frontend also reads in a file (current_bank_accounts_file.txt, this is currently nonfunctional and will be tested) and writes to a file 
(bank-transaction-file.txt) 

To demonstrate architecture for account operations, we use fictional accounts for the time being. This will be overhauled in the next iteration.

The frontend also processes other transactions, such as log-in, logout, and paying bills.
'''

# SESSION STATE
current_session = {
    "logged_in": False,
    "mode": None,          # "standard" or "admin"
    "account_holder": None # Only used in standard mode to control session transactions.
}

# Track total paid per company in session (standard mode restriction)
session_bill_totals = {
    "EC": 0.0,
    "CQ": 0.0,
    "FI": 0.0
}

#Companies allowed to receive bills.
VALID_COMPANIES = {
    "EC": "The Bright Light Electric Company (EC)",
    "CQ": "Credit Card Company Q (CQ)",
    "FI": "Fast Internet, Inc. (FI)"
}

#Function to parse current accounts file to validate login process.
def load_accounts_file(file, input_name, input_id):
    with open(file, "r") as f:
        for line in f:
            line = line.rstrip("\n")

            # Extract fields by fixed positions
            raw_id = line[0:5]
            name = line[6:26].strip()
            status = line[27]           # Type of Account
            raw_balance = line[-8:]

            # Stop at EOF marker
            if raw_id == "!0000":
                return (-1, "F")

            # Convert ID to int for comparison
            try:
                numeric_id = int(raw_id)
            except ValueError:
                continue

            if numeric_id == int(input_id) and input_name == name:
                return (float(raw_balance), status)

    return None

def does_Account_Exist(file, input_id):
    with open (file, 'r') as f:
        for line in f:
            line = line.rstrip("\n")
            
            #Process ID
            raw_id = line[0:5]

            try:
                numeric_id = int(raw_id)
            except ValueError:
                continue

            if numeric_id == int(input_id):
                return True
    
        return False

session_transactions = []  # stores formatted 40-char transaction lines

# FORMAT FUNCTIONS FOR TRANSACTION STORAGE
def format_alpha(field: str, length: int) -> str:
    return field.ljust(length)[:length]

def format_numeric(field: str, length: int) -> str:
    return str(field).zfill(length)[-length:]

def format_money(amount: float) -> str:
    return f"{amount:08.2f}"

# MAIN MENU

# This controls the main menu display. Each also returns a choice and mode to the front end to display the right amount.
def display_main_menu(test_mode=False):
    #Case 1: They are not logged in.
    if not current_session["logged_in"]:
        if not test_mode:
            print("\n<+= Banking System =+>")
            print("1. Login")
            print("2. Exit")

        while True:
            choice = input() if test_mode else input("Select an option: ")
            try:
                return int(choice), "a"
            except ValueError:
                if not test_mode: print("Invalid input. Please enter a number.")

    #Case 2: They are logged in as a non-privileged user.
    elif current_session["mode"] == "standard":
        if not test_mode:
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

        while True:
            choice = input() if test_mode else input("Select an option: ")
            try:
                return int(choice), "b"
            except ValueError:
                if not test_mode: print("Invalid input. Please enter a number.")
    
    #Case 3: They are logged in as an administrator.
    else:
        if not test_mode:
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
            print("10. Delete Account (Admin)")
            print("11. Disable Account (Admin)")
            print("12. Change Plan (Admin)")
            print("13. Exit")

        while True:
            choice = input() if test_mode else input("Select an option: ")
            try:
                return int(choice), "c"
            except ValueError:
                if not test_mode : print("Invalid input. Please enter a number.")


# RECORD TRANSACTIONS

def record_transaction(code: str,
                       account_holder: str = "",
                       account_number: str = "00000",
                       amount: float = 0.0,
                       misc: str = ""):
    """
    Creates and stores a properly formatted 40-character transaction line.
    """

    #Calls format functions to properly format string.
    CC = format_numeric(code, 2)
    AAAAA = format_alpha(account_holder, 20)
    NNNNN = format_numeric(account_number, 5)
    PPPPPPPP = format_money(amount)
    MM = format_alpha(misc, 2)

    line = f"{CC} {AAAAA} {NNNNN} {PPPPPPPP}{MM}"
    print(line)

    # Will be used later to determine if the transactions are properly formatted or not.

    # if len(line) != 40:
    #     raise ValueError("Transaction line is not 40 characters.")

    session_transactions.append(line)

# LOGIN
def handle_login(session_type: str, account_holder: str | None = None):
    """
    Returns: Success and/or error message (str)
    """
    global current_session

    # Checks if the mode is valid.
    if current_session["logged_in"]:
        return "Error: Already logged in. Please logout first."

    if session_type not in ["standard", "admin"]:
        return "Error: Invalid session type."

    if session_type == "standard" and not account_holder:
        return "Error: Standard login requires account holder name."
    
    #Sets current_session to the correct types.
    current_session["account_holder"] = account_holder
    current_session["logged_in"] = True
    current_session["mode"] = session_type

    return f"Login successful ({session_type} mode)."


# LOGOUT

def handle_logout():
    global current_session, session_bill_totals, session_transactions

    if not current_session["logged_in"]:
        return "Error: No active session."
    
    current_session["account_holder"] = ""

    # Add end-of-session record
    record_transaction("00")

    '''
    WRITING TO FILE DOES NOT WORK RIGHT NOW
    '''
    try:
        with open("./records/bank_transaction_file.txt", "a") as f:
            for line in session_transactions:
                f.write(line + "\n")
            print("Transactions:", session_transactions)
    except Exception as e:
        return f"Error writing transaction file: {str(e)}"

    # Reset session
    current_session = {
        "logged_in": False,
        "mode": None,
        "account_holder": None
    }

    session_bill_totals = { "EC": 0.0, "CQ": 0.0, "FI": 0.0 }
    session_transactions = []

    return "Logout successful. Transaction file written."

# ACCOUNT CREATION

def handle_create_account(name: str, initial_balance: float):
    """
    Returns: Success or error message (str)

    Expected backend call:
        controller.create_account(name, initial_balance)
    """
    global current_session

    if current_session["mode"] != "admin":
        return "Error: Privileged Transaction."

    try:
        acc_id = write_Account_To_File('../tests/current_accounts/currentaccounts.txt', name, initial_balance)

        record_transaction("05", name, acc_id, initial_balance) # REPLACE 0 WITH NEW ID
        
        return f"Account successfully created for {name}."
    except Exception as e:
        return f"Error creating account: {str(e)}"

def write_Account_To_File(file, name, balance):
    # Read all existing lines
    with open(file, "r") as f:
        lines = f.readlines()

    # Remove trailing newline-only lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    # Remove the last meaningful line (the delimiter)
    if lines:
        lines.pop()

    # Collect used IDs
    used_ids = set()
    for line in lines:
        line = line.rstrip("\n")
        if len(line) < 5:
            continue
        raw_id = line[0:5]
        try:
            used_ids.add(int(raw_id))
        except ValueError:
            continue

    # Pick the lowest unused ID
    new_id = 0
    while new_id in used_ids:
        new_id += 1

    # Format new account line
    id_str = f"{new_id:05}"
    name_field = name.ljust(20)[:20]
    balance_field = f"{balance:08.2f}"
    new_line = f"{id_str} {name_field} A {balance_field}\n"

    # Rebuild file: all lines except old delimiter, then new account, then delimiter
    with open(file, "w") as f:
        for line in lines:
            f.write(line)
        f.write(new_line)
        f.write("!0000 END_OF_FILE\n")
    return new_id


# DEPOSIT

def handle_deposit(account_id: str, amount: float):
    """
    Returns: Success or error message (str)
    """
    global current_session

    balance, account_type = load_accounts_file('../tests/current_accounts/currentaccounts.txt', current_session["account_holder"], account_id)

    #Checks if account exists
    if (account_type == "F"):
        return f"Error: Account does not exist."

    record_transaction("04", "John Doe", account_id, amount) # SWAP JOHN DOE WITH account name from account id
    try:
        # controller.deposit(account_id, amount)
        return "Deposit successful."
    except Exception as e:
        return f"Deposit failed: {str(e)}"


# WITHDRAW

def handle_withdraw(account_id: str, amount: float, account_owner: str | None=None):
    """
    Returns: Success or error message (str)
    """
    global current_session

    #If standard, sets it to be correct
    if account_owner == None:
        account_owner = current_session['account_holder']

    #Checks if the amount is allowed to be withdrawn ($500 limit)
    if (amount > 500):
        return f"Error: {amount} exceeds your limit of $500."
    
    #Checks if the amount is less than your equal to your balance (Overdraft)
    balance, account_type = load_accounts_file('../tests/current_accounts/currentaccounts.txt', account_owner, account_id)

    #Checks if account exists
    if (account_type == "F"):
        return f"Error: Account does not exist."
    
    if (amount > balance):
        return f"Error: Cannot overdraft."

    record_transaction("01", account_owner, account_id, amount) # SWAP JOHN DOE WITH account name from account id
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
    global current_session

    #Check you own the source account
    balance, accountType = load_accounts_file('../tests/current_accounts/currentaccounts.txt', current_session["account_holder"], src_id)
    if (accountType == "F"):
        return "Error: You must own the account you intend to transfer from."

    #Check that both accounts exist
    if not (does_Account_Exist('../tests/current_accounts/currentaccounts.txt', src_id) 
            or does_Account_Exist('../tests/current_accounts/currentaccounts.txt', dest_id)):
            return "Error: One or more accounts do not exist."
    
    #Check the transaction is not greater than $1000
    if (amount > 1000):
        return "Error: Cannot transfer more than $1000."
    
    #Check that the transfer does not overdraft.
    if (amount > balance):
        return "Error: Cannot transfer more than you own."

    record_transaction("02", current_session["account_holder"], src_id, amount, str(int(dest_id))) # SWAP JOHN DOE WITH account name from account id
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
    global current_session, session_bill_totals

    #Uses the current user information if they are logged in.
    if account_holder == None:
        account_holder = current_session["account_holder"]

    #Does not work if the user is not logged in.
    if not current_session["logged_in"]:
        return "Error: You must login first."

    #If the user selects an invalid target.
    if company_code not in VALID_COMPANIES:
        return "Error: Invalid company."

    #If the user pays a zero/negative amount.
    if amount <= 0:
        return "Error: Invalid payment amount. Our CEOs will starve to death."
    
    #If the user pays over $2000.
    if amount > 2000:
        return "Error: Bill paid cannot exceed $2000."

    record_transaction("03", account_holder, account_number, amount, company_code)

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


# Authentication function

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

# DELETE ACCOUNT

def handle_delete_account(account_holder: str, account_number: str):
    """
    Constraints:
        - Admin only
        - Account holder must exist
        - Account number must match holder
        - No further transactions allowed on deleted account
    """

    if not current_session["logged_in"]:
        return "Error: You must login first."

    if current_session["mode"] != "admin":
        return "Error: Delete is a privileged transaction (admin only)."

    if not account_holder or not account_number:
        return "Error: Account holder and account number required."

    record_transaction("06", account_holder, account_number)

    try:
        # controller.delete_account(account_holder, account_number)
        # Backend should:
        # - Validate holder exists
        # - Validate account belongs to holder
        # - Mark account as deleted
        # - Prevent future transactions
        # - Save transaction record

        return f"Account {account_number} deleted successfully."

    except Exception as e:
        return f"Delete failed: {str(e)}"

# DISABLE ACCOUNT

def handle_disable_account(account_holder: str, account_number: str):
    """
    Constraints:
        - Admin only
        - Must be valid account
        - No further transactions allowed on disabled account
    """

    if not current_session["logged_in"]:
        return "Error: You must login first."

    if current_session["mode"] != "admin":
        return "Error: Disable is a privileged transaction (admin only)."

    if not account_holder or not account_number:
        return "Error: Account holder and account number required."

    record_transaction("07", account_holder, account_number)

    try:
        # controller.disable_account(account_holder, account_number)
        # Backend should:
        # - Verify account exists
        # - Verify ownership
        # - Change status A -> D
        # - Save transaction

        return f"Account {account_number} disabled successfully."

    except Exception as e:
        return f"Disable failed: {str(e)}"

# CHANGE PLAN (STUDENT/NON)

def handle_change_plan(account_holder: str, account_number: str):
    """
    Constraints:
        - Admin only
        - Account must exist
        - Must belong to specified holder
    """

    if not current_session["logged_in"]:
        return "Error: You must login first."

    if current_session["mode"] != "admin":
        return "Error: ChangePlan is a privileged transaction (admin only)."

    if not account_holder or not account_number:
        return "Error: Account holder and account number required."

    record_transaction("08", account_holder, account_number)

    try:
        # controller.change_plan(account_holder, account_number)
        # Backend should:
        # - Verify account exists
        # - Verify ownership
        # - Change plan SP <-> NP
        # - Save transaction

        return f"Payment plan updated for account {account_number}."

    except Exception as e:
        return f"ChangePlan failed: {str(e)}"
