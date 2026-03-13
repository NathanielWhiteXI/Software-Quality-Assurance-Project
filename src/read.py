def read_old_bank_accounts(file_path):
    """
    Reads and validates the Master Bank Accounts file.

    Format:
    NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP_TTTT

    Returns:
        list of account dictionaries
    """

    accounts = []

    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):

            clean_line = line.rstrip('\n')

            # Validate line length
            if len(clean_line) != 42:
                print(f"ERROR: Fatal error - Line {line_num}: Invalid length ({len(clean_line)} chars, expected 42)")
                continue

            try:
                # Extract fields
                account_number = clean_line[0:5]
                name = clean_line[6:26]
                status = clean_line[27]
                balance_str = clean_line[29:37]
                transactions_str = clean_line[38:42]

                # Validate spaces in correct positions
                if clean_line[5] != ' ' or clean_line[26] != ' ' or clean_line[28] != ' ' or clean_line[37] != ' ':
                    print(f"ERROR: Fatal error - Line {line_num}: Incorrect spacing format")
                    continue

                # Validate account number (5 digits)
                if not account_number.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Account number must be 5 digits")
                    continue

                # Validate status
                if status not in ('A', 'D'):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid status '{status}'")
                    continue

                # Validate balance format (XXXXX.XX)
                if (
                    len(balance_str) != 8 or
                    balance_str[5] != '.' or
                    not balance_str[:5].isdigit() or
                    not balance_str[6:].isdigit()
                ):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid balance format '{balance_str}'")
                    continue

                # Validate transactions
                if not transactions_str.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Transaction count must be 4 digits")
                    continue

                # Convert values
                balance = float(balance_str)
                transactions = int(transactions_str)

                # Business rule validation
                if balance < 0:
                    print(f"ERROR: Fatal error - Line {line_num}: Negative balance detected")
                    continue

                if transactions < 0:
                    print(f"ERROR: Fatal error - Line {line_num}: Negative transactions not allowed")
                    continue

                accounts.append({
                    "account_number": account_number,
                    "name": name.rstrip(),
                    "status": status,
                    "balance": balance,
                    "total_transactions": transactions
                })

            except Exception as e:
                print(f"ERROR: Fatal error - Line {line_num}: Unexpected error - {str(e)}")

    # Ensure accounts are sorted by account number
    accounts.sort(key=lambda acc: int(acc["account_number"]))

    return accounts