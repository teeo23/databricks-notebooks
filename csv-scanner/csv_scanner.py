import pandas as pd
import os
import re

csv_path = os.path.expanduser("~/Downloads/National_Statistics_Postcode_Lookup_UK_20251007.csv")  

df = pd.read_csv(csv_path)
#print(df.head())
print("CSV loaded successfully")

#Check for URL's
url_pattern = re.compile(r'(https?://[^\s]+)', re.IGNORECASE)

#Check for formula triggers
formula_triggers = ('=', '+', '@', '|')

formula_like_re = re.compile(
    r'^\s*=\s*(?:'
    r'[A-Za-z_][A-Za-z0-9_]*\s*\('                  # =FUNCTION(
    r'|\$?[A-Za-z]{1,3}\$?\d+'                       # =A1 or =$B$5
    r'|\'[^\'\n]+\'!?\$?[A-Za-z]{1,3}\$?\d+'         # ='Sheet 1'!A1
    r')',
    re.IGNORECASE
)


sql_keywords = [
    "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
    "UNION", "INTO", "VALUES", "FROM", "WHERE", "JOIN", "HAVING",
    "GROUP", "ORDER", "LIMIT", "OFFSET", "EXEC", "EXECUTE", "MERGE",
    "GRANT", "REVOKE", "CALL", "DESCRIBE", "SHOW"
]

sql_re = re.compile(r'\b(' + r'|'.join(sql_keywords) + r')\b', re.IGNORECASE)
sql_comment_re = re.compile(r'(^|\s)--\s?.*')

url_found = False
asterisks_found = False
formula_triggers_found = False
formulas_found = False
sql_found = False

for i, row in df.iterrows():
    for col in df.columns:
        cell_value = str(row[col])
        urls = url_pattern.findall(cell_value)
        if urls:
            found_any = True
            print(f"Found URL(s) in row {i + 1}, column '{col}': {urls}")

        if '*' in cell_value:
            asterisks_found = True
            print(f"✳️ Found '*' in row {i + 1}, column '{col}': {cell_value}")

        if cell_value.startswith(formula_triggers):
            formula_triggers_found = True
            print(f"Found formula triggering cell in row {i + 1}, column '{col}': {cell_value}")

        if formula_like_re.match(cell_value):
            formulas_found = True
            print(f"Found formulas in row {i + 1}, column '{col}': {cell_value}")

        if sql_re.search(cell_value) or sql_comment_re.search(cell_value):
            sql_found = True
            print(f"Found possible SQL content in row {i + 1}, column '{col}': {cell_value}")


if not url_found :
    print("No URLs found in the CSV file.")
else:
    print("URL scan completed.")

if not asterisks_found:
    print("No '*' characters found in the CSV file.")
else:
    print("Asterisk scan completed.")

if not formula_triggers_found:
    print("No formula triggering cells found in the CSV file.")
else:
    print("Formula triggers scan completed.")

if not formulas_found:
    print("No formulas found in the CSV file.")
else:
    print("Formula scan completed.")

if not sql_found:
    print("No SQL-like content found in the CSV file.")
else:
    print("SQL scan completed.")