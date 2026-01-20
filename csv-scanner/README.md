# CSV Security Scanner

A simple Python script that scans a CSV file for potentially unsafe or unexpected content.  
The script **only reads and reports** — it does not modify the CSV.

## What this script checks

For every cell in the CSV file, the script scans for:

### 1. URLs
- Detects `http://` and `https://` links anywhere in a cell.

### 2. Asterisk character
- Flags any cell containing the `*` character.

### 3. Formula-triggering characters
- Flags cells that **start with** one of the following characters:
  - `=`, `+`, `@`, `|`
- These characters can cause spreadsheet software (e.g. Excel) to interpret a value as a formula.
- This check is **separate** from formula detection and may include legitimate values such as negative numbers or coordinates.

### 4. Spreadsheet formulas (heuristic detection)
- Flags cells that appear to contain actual spreadsheet formulas, such as:
  - Function calls: `=SUM(A1:A5)`
  - Cell references: `=A1+B2`, `=$B$5`
  - Sheet-qualified references: `='Sheet 1'!A1`
- This uses a heuristic regex and is intentionally conservative.

### 5. SQL-like content
- Flags cells containing common SQL keywords such as:
  - `SELECT`, `DROP`, `DELETE`, `INSERT`, etc.
- Also flags SQL-style inline comments using `--`.

## Requirements

- Python 3.9+
- pandas
