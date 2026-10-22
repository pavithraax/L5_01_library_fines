# Lab 5: Static Code Analysis — Issues

The original `library_system.py` was analyzed using Pylint, Bandit, and Flake8. The following issues were identified and prioritized by severity.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe use of `eval()` | Security — Medium | 45 | Evaluates a dynamically constructed expression, which can execute unintended code. | Replaced it with an AST-based evaluator that allows only basic arithmetic operations and the `days` variable. |
| Bare exception handling | Code quality | 21 | The bare `except` catches all exceptions and silently hides unexpected errors. | Catch only `KeyError` and `ValueError`, which can occur when the requested loan or book is missing. |
| Mutable default argument | Bug risk | 9 | The default `dates=[]` is shared across calls, so dates may accumulate unexpectedly. | Changed the default to `None` and initialized a new list inside the function. |
| Unused import | Style | 2 | The `os` module is imported but never used. | Removed the unused import. |
| Global state modification | Maintainability | 28, 35 | Functions modify global variables, making behavior harder to track and test. | Removed the global fine-rate modification from renewal handling and reduced global reassignment in record loading. |
| Unsafe file handling | Code quality | 34–41 | Files are opened without context managers or explicit encodings. | Used `with` statements and UTF-8 encoding for file operations. |
| Missing docstrings | Code quality | 1, 9, 16, 24, 27, 33, 39, 44, 47, 52 | The module and functions lack documentation. | Added a module docstring and function docstrings. |
| Inconsistent function naming | Style | 27 | `renewBook` does not follow Python's snake_case naming convention. | Renamed the function to `renew_book`. |
| Negative overdue days | Logic bug | 68 | Negative overdue days result in a negative fine. | Used `max(0, days_overdue)` so the fine cannot be negative. |
| Inconsistent formatting | Style | 14, 31, 68 | Old-style string formatting, long lines and spacing violations reduce readability. | Used f-strings, wrapped long statements and formatted the file consistently. |

## Summary

The changes focus on security, predictable behavior, readability, and maintainability while retaining the core library-loan functionality. The final version must be checked again using all three static analysis tools to verify which findings have been resolved.