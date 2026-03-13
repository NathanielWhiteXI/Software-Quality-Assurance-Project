# -----------------------------
# BACKEND = CONTROLLER
# -----------------------------

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from read import *
from write import *
from print_error import *

ACCOUNTS_FILE = os.path.join(
    BASE_DIR,
    "..",
    "tests",
    "current_accounts",
    "currentaccounts.txt"
)


# EVERYTHING BEYOND THIS POINT MAY NOT WORK

# -----------------------------
# INTERNAL HELPERS
# -----------------------------

def load_accounts():
    return read_old_bank_accounts(ACCOUNTS_FILE)


def save_accounts(accounts):
    write_new_current_accounts(accounts, ACCOUNTS_FILE)


def find_account(accounts, account_number):
    for acc in accounts:
        if acc["account_number"] == str(int(account_number)):
            return acc
    return None


def verify_account_owner(account, name):
    return account["name"] == name


# -----------------------------
# ACCOUNT OPERATIONS
# -----------------------------

def create_account(name, initial_balance):
    accounts = load_accounts()

    new_id = 0
    used_ids = {int(acc["account_number"]) for acc in accounts}

    while new_id in used_ids:
        new_id += 1

    new_account = {
        "account_number": str(new_id),
        "name": name,
        "status": "A",
        "balance": float(initial_balance),
        "total_transactions": 0,
        "plan": "NP"
    }

    accounts.append(new_account)

    save_accounts(accounts)

    return str(new_id)


def deposit(account_number, amount):
    accounts = load_accounts()

    acc = find_account(accounts, account_number)
    if not acc:
        raise Exception("Account not found")

    if acc["status"] != "A":
        raise Exception("Account disabled")

    acc["balance"] += amount
    acc["total_transactions"] += 1

    save_accounts(accounts)


def withdraw(account_number, amount):
    accounts = load_accounts()

    acc = find_account(accounts, account_number)
    if not acc:
        raise Exception("Account not found")

    if acc["status"] != "A":
        raise Exception("Account disabled")

    if acc["balance"] < amount:
        raise Exception("Insufficient funds")

    acc["balance"] -= amount
    acc["total_transactions"] += 1

    save_accounts(accounts)


def transfer(src_account, dest_account, amount):
    accounts = load_accounts()

    src = find_account(accounts, src_account)
    dst = find_account(accounts, dest_account)

    if not src or not dst:
        raise Exception("Account not found")

    if src["balance"] < amount:
        raise Exception("Insufficient funds")

    src["balance"] -= amount
    dst["balance"] += amount

    src["total_transactions"] += 1
    dst["total_transactions"] += 1

    save_accounts(accounts)


def pay_bill(account_holder, account_number, company, amount):
    accounts = load_accounts()

    acc = find_account(accounts, account_number)
    if not acc:
        raise Exception("Account not found")

    if not verify_account_owner(acc, account_holder):
        raise Exception("Account does not belong to user")

    if acc["balance"] < amount:
        raise Exception("Insufficient funds")

    acc["balance"] -= amount
    acc["total_transactions"] += 1

    save_accounts(accounts)


# -----------------------------
# ADMIN OPERATIONS
# -----------------------------

def delete_account(account_holder, account_number):
    accounts = load_accounts()

    acc = find_account(accounts, account_number)
    if not acc:
        raise Exception("Account not found")

    if not verify_account_owner(acc, account_holder):
        raise Exception("Owner mismatch")

    accounts.remove(acc)

    save_accounts(accounts)


def disable_account(account_holder, account_number):
    accounts = load_accounts()

    acc = find_account(accounts, account_number)
    if not acc:
        raise Exception("Account not found")

    if not verify_account_owner(acc, account_holder):
        raise Exception("Owner mismatch")

    acc["status"] = "D"

    save_accounts(accounts)


def change_plan(account_holder, account_number):
    accounts = load_accounts()

    acc = find_account(accounts, account_number)
    if not acc:
        raise Exception("Account not found")

    if not verify_account_owner(acc, account_holder):
        raise Exception("Owner mismatch")

    if acc["plan"] == "NP":
        acc["plan"] = "SP"
    else:
        acc["plan"] = "NP"

    save_accounts(accounts)


# -----------------------------
# QUERY OPERATIONS
# -----------------------------

def get_account(account_number):
    accounts = load_accounts()

    acc = find_account(accounts, account_number)

    if not acc:
        raise Exception("Account not found")

    return acc


def get_all_accounts():
    return load_accounts()

# Testing
if __name__ == "__main__":
    get_all_accounts()