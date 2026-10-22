
"""Manage library loans, renewals, and overdue fines."""

import ast
import json
import operator
from datetime import datetime
from pathlib import Path

loans = {}
FINE_PER_DAY = 2

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def add_book_loan(student_id, book_id, dates=None):
    """Record a book loan for a student."""
    if not student_id:
        return

    if dates is None:
        dates = []

    dates.append(str(datetime.now()))
    loans.setdefault(student_id, []).append(str(book_id))
    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Remove a returned book from a student's loans."""
    try:
        loans[student_id].remove(book_id)
    except (KeyError, ValueError):
        return

    if not loans[student_id]:
        del loans[student_id]


def calculate_fine(days_overdue):
    """Calculate the fine for overdue days."""
    return max(0, days_overdue) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Print the renewal details for a borrowed book."""
    print(
        f"Renewed {book_id} for {student_id} "
        f"by {extra_days} days"
    )


def _evaluate_rule(node, days):
    """Evaluate a restricted arithmetic expression."""
    if isinstance(node, ast.Expression):
        return _evaluate_rule(node.body, days)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.Name) and node.id == "days":
        return days

    if isinstance(node, ast.BinOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None or isinstance(node.op, (ast.UAdd, ast.USub)):
            raise ValueError("Unsupported operator")

        left = _evaluate_rule(node.left, days)
        right = _evaluate_rule(node.right, days)
        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported unary operator")
        return operation(_evaluate_rule(node.operand, days))

    raise ValueError("Unsupported expression in fine rule")


def fine_from_rule(rule, days):
    """Calculate a fine from a restricted arithmetic rule."""
    try:
        expression = ast.parse(rule, mode="eval")
        return _evaluate_rule(expression, days)
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as error:
        raise ValueError("Invalid fine rule") from error


def load_records(file="loans.json"):
    """Load loan records from a JSON file."""
    with Path(file).open("r", encoding="utf-8") as record_file:
        records = json.load(record_file)

    if not isinstance(records, dict):
        raise ValueError("Loan records must contain a JSON object")

    loans.clear()
    loans.update(records)


def save_records(file="loans.json"):
    """Save loan records to a JSON file."""
    with Path(file).open("w", encoding="utf-8") as record_file:
        json.dump(loans, record_file, indent=2)


def print_report():
    """Print all current loan records."""
    print("Loan Report")
    for student_id, book_ids in loans.items():
        print(f"{student_id} -> {book_ids}")


def main():
    """Run the library loan demonstration."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)

    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))

    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    try:
        overdue_days = int(days)
    except ValueError:
        print("Please enter a whole number of days.")
        return

    print("S102 owes:", calculate_fine(overdue_days))
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
