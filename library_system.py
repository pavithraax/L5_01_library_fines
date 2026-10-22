"""Library loan management and fine calculation system."""

import ast
import json
import operator
from datetime import datetime

loans = {}
FINE_PER_DAY = 2
BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}


def add_book_loan(student_id, book_id, dates=None):
    """Record a book loan and its date."""
    if not student_id:
        return

    if dates is None:
        dates = []

    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [str(book_id)]
    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Return a book if the student has borrowed it."""
    if student_id not in loans or book_id not in loans[student_id]:
        return

    loans[student_id].remove(book_id)
    if not loans[student_id]:
        del loans[student_id]


def calculate_fine(days_overdue):
    """Calculate a fine for the supplied number of overdue days."""
    return max(0, days_overdue) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Renew a book and adjust the fine rate for long renewals."""
    global FINE_PER_DAY

    if extra_days > 14:
        FINE_PER_DAY += 1

    print(
        f"Renewed {book_id} for {student_id} "
        f"by {extra_days} days"
    )


def load_records(file="loans.json"):
    """Load loan records from a JSON file."""
    with open(file, "r", encoding="utf-8") as records_file:
        records = json.load(records_file)

    if not isinstance(records, dict):
        raise ValueError("Loan records must be a JSON object.")

    loans.clear()
    loans.update(records)


def save_records(file="loans.json"):
    """Save loan records to a JSON file."""
    with open(file, "w", encoding="utf-8") as records_file:
        json.dump(loans, records_file, indent=2)


def evaluate_expression(node, days):
    """Evaluate a restricted arithmetic expression safely."""
    if isinstance(node, ast.Expression):
        return evaluate_expression(node.body, days)

    if isinstance(node, ast.Name) and node.id == "days":
        return days

    if (
        isinstance(node, ast.Constant)
        and type(node.value) in (int, float)
    ):
        return node.value

    if isinstance(node, ast.BinOp):
        operation = BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported arithmetic operator.")

        left = evaluate_expression(node.left, days)
        right = evaluate_expression(node.right, days)
        return operation(left, right)

    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub)
    ):
        value = evaluate_expression(node.operand, days)
        return value if isinstance(node.op, ast.UAdd) else -value

    raise ValueError("Invalid fine calculation rule.")


def fine_from_rule(rule, days):
    """Calculate a fine using a restricted arithmetic rule."""
    try:
        expression = ast.parse(rule, mode="eval")
    except (SyntaxError, TypeError) as error:
        raise ValueError("Invalid fine calculation rule.") from error

    return evaluate_expression(expression, days)


def print_report():
    """Print all current student loan records."""
    print("Loan Report")
    for student_id, book_ids in loans.items():
        print(f"{student_id} -> {book_ids}")


def main():
    """Run a demonstration of the library loan system."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)

    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))

    days_input = input("Days overdue for S102 (press Enter for 0): ")
    try:
        days = int(days_input or "0")
        print("S102 owes:", calculate_fine(days))
    except ValueError:
        print("Please enter a valid whole number.")

    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
