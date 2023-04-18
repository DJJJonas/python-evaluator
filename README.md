# Expression evaluator

## Compute the value of a mathematical expression and check for errors.

Supported operators:
| Operator    | Description        |
| ----------- | ------------------ |
| \+ Plus     | `0.1 + 0.2 == 0.3` |
| \- Minus    | `10 - 4 == -6`     |
| \* Multiply | `2 * 3 == 6`       |
| / Divide    | `10 / 2 == 5`      |
| \^ Exponent | `2 ^ 3 == 8`       |
| \ Root of   | `2 \ 16 == 4`      |

_Parenthesis are not supported yet._

```
>>> calculate("2 + 3 * 4 / 2 - 1")
(9.0, None)
>>> calculate("2 + 3 * / 2 - 1")
(0.0, "Invalid syntax at position 7: Invalid expression. Can't multiply 3 and /")

```
