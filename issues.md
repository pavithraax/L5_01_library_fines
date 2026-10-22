# Static Code Analysis - Issues Found

| Issue | Type | Line(s) | Description | Fix |
|---|---|---|---|---|
| Unsafe `eval()` | Security | 45 | Could execute unwanted Python code. | Replaced it with a safe arithmetic evaluator. |
| Mutable default argument | Bug | 9 | The default list could be shared between function calls. | Changed `[]` to `None`. |
| Bare `except` | Code quality | 21 | Silently ignored all exceptions. | Added a check before removing a book. |
| Missing docstrings | Code quality | Multiple | Functions did not explain what they do. | Added short docstrings. |
| Unused import | Style | 2 | The `os` module was not used. | Removed the import. |
| File handling | Code quality | 34-41 | Files were opened without specifying encoding or using `with`. | Used `with open()` and UTF-8 encoding. |
| Formatting issues | Style | Multiple | Incorrect spacing, long lines and naming issues. | Fixed formatting and used snake_case names. |

## Result

- Pylint score improved from 6.07 to 9.89.
- Bandit reported no issues after the fixes.
- Flake8 reported no violations after the fixes.
