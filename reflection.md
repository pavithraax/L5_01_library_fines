# Lab 5: Reflection

### 1. What is static code analysis, and why is it useful?

Static code analysis checks source code without executing it. It helps identify possible bugs, security risks, and coding-style problems early, making programs easier to maintain.

### 2. What did Pylint, Bandit, and Flake8 help identify?

Pylint identified code-quality issues such as missing docstrings, mutable default arguments, global statements, and inconsistent naming. Bandit identified the use of `eval()` and overly broad exception handling. Flake8 identified formatting violations, long lines, and an unused import.

### 3. Which issues were most important, and how were they fixed?

The unsafe use of `eval()` was the most important security concern because it could execute unintended expressions. It was replaced with a restricted arithmetic evaluator. The mutable default argument was replaced with `None`, broad exception handling was narrowed, and file operations were updated to use context managers and explicit UTF-8 encoding.

### 4. How did static analysis improve the program?

The tools helped improve security, readability, and maintainability. The final program also handles negative overdue days correctly and validates user input. Running the tools again helped verify whether the reported issues had been resolved.
