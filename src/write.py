def write_new_current_accounts(accounts, file_path):
    """
    Writes the Master Bank Accounts File.

    Format:
    NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT

    Constraints:
    - 42 characters per line
    - numeric fields zero padded
    - alphabetic fields space padded
    - sorted by account number
    """

    # Ensure ascending order
    accounts = sorted(accounts, key=lambda acc: int(acc['account_number']))

    with open(file_path, 'w') as file:
        for acc in accounts:

            # Validate account number
            acc_num = str(acc['account_number'])
            if not acc_num.isdigit() or len(acc_num) > 5:
                raise ValueError(f"Invalid account number: {acc_num}")

            # Validate name
            name = acc['name']
            if len(name) > 20:
                raise ValueError(f"Account name exceeds 20 characters: {name}")

            # Validate status
            status = acc['status']
            if status not in ('A', 'D'):
                raise ValueError(f"Invalid status: {status}")

            # Validate balance
            balance = acc['balance']
            if not isinstance(balance, (int, float)):
                raise ValueError(f"Balance must be numeric: {balance}")

            if balance < 0 or balance > 99999.99:
                raise ValueError(f"Invalid balance: {balance}")

            # Validate transactions
            transactions = acc['total_transactions']
            if not isinstance(transactions, int):
                raise ValueError(f"Transactions must be integer: {transactions}")

            if transactions < 0 or transactions > 9999:
                raise ValueError(f"Invalid transaction count: {transactions}")

            # Format fields
            acc_num_fmt = acc_num.zfill(5)
            name_fmt = name.ljust(20)[:20]
            balance_fmt = f"{balance:08.2f}"
            trans_fmt = str(transactions).zfill(4)

            line = f"{acc_num_fmt} {name_fmt} {status} {balance_fmt} {trans_fmt}"

            # Final safety check
            if len(line) != 42:
                raise ValueError(f"Line formatting error: '{line}' length={len(line)}")

            file.write(line + "\n")