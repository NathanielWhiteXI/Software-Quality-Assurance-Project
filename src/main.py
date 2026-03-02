import sys
import frontend

def main():
    if len(sys.argv) < 3:
        sys.exit(1)

    accounts_file = sys.argv[1]
    trans_out_file = sys.argv[2]
    test_mode = "-t" in sys.argv

    frontend.set_runtime_config(accounts_file, trans_out_file, test_mode)

    for raw in sys.stdin:
        cmd = raw.strip().lower()
        if cmd == "":
            continue

        if cmd == "login":
            mode = sys.stdin.readline().strip().lower()
            name = sys.stdin.readline().strip()
            if mode == "admin":
                frontend.handle_login("admin")
            else:
                frontend.handle_login("standard", name)
            continue

        if cmd == "logout":
            frontend.handle_logout()
            continue

        if cmd == "withdrawal":
            acc = sys.stdin.readline().strip()
            amt = float(sys.stdin.readline().strip())
            frontend.handle_withdraw(acc, amt)
            continue

        if cmd == "transfer":
            src = sys.stdin.readline().strip()
            dst = sys.stdin.readline().strip()
            amt = float(sys.stdin.readline().strip())
            frontend.handle_transfer(src, dst, amt)
            continue

        if cmd == "paybill":
            if frontend.current_session.get("mode") == "admin":
                holder = sys.stdin.readline().strip()
            else:
                holder = None
            acc = sys.stdin.readline().strip()
            company = sys.stdin.readline().strip().upper()
            amt = float(sys.stdin.readline().strip())
            frontend.handle_paybill(acc, company, amt, holder)
            continue

        if cmd == "create":
            name = sys.stdin.readline().strip()
            amt = float(sys.stdin.readline().strip())
            frontend.handle_create_account(name, amt)
            continue

        if cmd == "delete":
            holder = sys.stdin.readline().strip()
            acc = sys.stdin.readline().strip()
            frontend.handle_delete_account(holder, acc)
            continue

        if cmd == "disable":
            holder = sys.stdin.readline().strip()
            acc = sys.stdin.readline().strip()
            frontend.handle_disable_account(holder, acc)
            continue

        if cmd == "changeplan":
            holder = sys.stdin.readline().strip()
            acc = sys.stdin.readline().strip()
            frontend.handle_change_plan(holder, acc)
            continue

if __name__ == "__main__":
    main()