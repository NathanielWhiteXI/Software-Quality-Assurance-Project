import sys
from pathlib import Path
import pytest

# Allow imports from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import backend
from read import read_old_bank_accounts


def _write_accounts_file(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines)
    if lines:
        text += "\n"
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def temp_accounts_file(tmp_path, monkeypatch):
    accounts_file = tmp_path / "masteraccounts.txt"
    _write_accounts_file(
        accounts_file,
        [
            "00001 John Smith           A 00150.00 0003",
            "00002 Alice Johnson        A 00500.00 0012",
            "00003 Bob Lee              D 00000.00 0000",
            "00010 Maria Gonzalez       A 02340.50 0045",
            "00023 David Brown          A 00075.25 0007",
            "00100 Emily Chen           A 15000.00 0123",
            "00250 Michael Patel        D 00010.00 0001",
            "01000 Sarah Williams       A 00200.00 0025",
            "05000 Daniel Garcia        A 00001.00 0001",
            "99999 Test Account         D 00000.00 0000",
        ],
    )
    monkeypatch.setattr(backend, "ACCOUNTS_FILE", str(accounts_file))
    return accounts_file


# -----------------------------
# Method 1: transfer()
# Coverage target: statement coverage
# -----------------------------

def test_transfer_valid_updates_both_accounts_and_transaction_counts(temp_accounts_file):
    backend.transfer("00001", "00002", 50.0)

    src = backend.get_account("00001")
    dst = backend.get_account("00002")

    assert src["balance"] == pytest.approx(100.0)
    assert dst["balance"] == pytest.approx(550.0)
    assert src["total_transactions"] == 4
    assert dst["total_transactions"] == 13


def test_transfer_raises_when_source_or_destination_account_missing(temp_accounts_file):
    with pytest.raises(Exception, match="Account not found"):
        backend.transfer("00001", "77777", 10.0)


def test_transfer_raises_when_insufficient_funds(temp_accounts_file):
    with pytest.raises(Exception, match="Insufficient funds"):
        backend.transfer("05000", "00001", 2.0)


# -----------------------------
# Method 2: read_old_bank_accounts()
# Coverage target: decision and loop coverage
# -----------------------------

def test_read_old_bank_accounts_filters_invalid_lines_and_sorts_valid_accounts(tmp_path):
    accounts_file = tmp_path / "mixed_accounts.txt"
    _write_accounts_file(
        accounts_file,
        [
            # valid
            "00010 Maria Gonzalez       A 02340.50 0045",
            # invalid length
            "SHORT LINE",
            # valid but out of order to verify sorting after loop finishes
            "00002 Alice Johnson        A 00500.00 0012",
            # incorrect spacing / non-digit account number
            "0000X John Smith           A 00150.00 0003",
            # invalid status
            "00011 Invalid Status       X 00100.00 0001",
            # invalid balance format
            "00012 Wrong Balance        A 0010A.00 0001",
            # invalid transactions
            "00013 Wrong Transactions   A 00010.00 00A1",
            # another valid line
            "00001 John Smith           A 00150.00 0003",
        ],
    )

    accounts = read_old_bank_accounts(str(accounts_file))

    assert [acc["account_number"] for acc in accounts] == ["00001", "00002", "00010"]
    assert [acc["name"] for acc in accounts] == ["John Smith", "Alice Johnson", "Maria Gonzalez"]
    assert [acc["status"] for acc in accounts] == ["A", "A", "A"]
    assert [acc["balance"] for acc in accounts] == [150.0, 500.0, 2340.50]
    assert [acc["total_transactions"] for acc in accounts] == [3, 12, 45]


def test_read_old_bank_accounts_returns_empty_list_for_empty_file(tmp_path):
    accounts_file = tmp_path / "empty_accounts.txt"
    accounts_file.write_text("", encoding="utf-8")

    assert read_old_bank_accounts(str(accounts_file)) == []