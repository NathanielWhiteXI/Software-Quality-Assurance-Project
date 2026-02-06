banking-system/
│
├── README.md
├── DESIGN.md
├── .gitignore
├── UML Diagram.drawio
├── UML Diagram.png
│
├── src/
│   ├── user.py
│   ├── frontend.py
│   ├── backend.py
│   └── main.py
│
├── data/
│   ├── accounts.txt
│   ├── master_accounts.txt
│   └── transactions.log
│
├── tests/
│   ├── current_accounts/
│   │   └── currentaccounts.txt
│   │
│   ├── inputs/
│   │   ├── T01_login_logout_standard.txt
│   │   ├── T02_withdraw_before_login.txt
│   │   ├── T03_double_login.txt
│   │   ├── ...
│   │
│   ├── expected_txt/
│   │   ├── T01_login_logout_standard.txt
│   │   ├── T02_withdraw_before_login.txt
│   │   ├── ...
│   │
│   └── test_transactions.py
│
├── scripts/
│   ├── run_all.sh
│   └── check_all.sh

## Architecture
The system follows a FrontEnd / BackEnd separation.

- FrontEnd handles:
  - User interaction
  - Input validation
  - Transaction file generation

- BackEnd handles:
  - Batch processing
  - Constraint enforcement
  - Persistent data updates

## Data Flow
User → FrontEnd → Transaction File → BackEnd → Updated Master File