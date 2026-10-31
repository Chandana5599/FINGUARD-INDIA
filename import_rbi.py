
import csv
import getpass
import mysql.connector

CSV_FILE = "dataset/RBI_import_clean.csv"

def number(value):
    value = (value or "").strip().replace(",", "")
    if value in ("", "-", "—", "NA", "N/A"):
        return None
    return float(value)

connection = None

try:
    password = getpass.getpass("Enter MySQL root password: ")

    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=1234,
        database="finguard"
    )

    cursor = connection.cursor()

    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required = {
            "Year", "Bank_ID", "Bank_Name",
            "Gross_Open", "Gross_Close", "Net_Open", "Net_Close",
            "Advances", "Tier1", "Tier2", "CAR",
            "Interest_Earned", "Interest_Expended", "NII",
            "Other_Income", "Operating_Expenses", "Net_Profit",
            "Assets", "Previous_Assets", "Borrowings",
            "Capital", "Reserves", "Deposits"
        }

        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("CSV headings do not match the expected columns.")

        banks = set()
        records = []

        for row in reader:
            bank_id = (row["Bank_ID"] or "").strip()
            bank_name = (row["Bank_Name"] or "").strip()

            if not bank_id or not bank_name:
                continue

            banks.add((bank_id, bank_name))

            records.append((
                bank_id,
                int(row["Year"]),
                number(row["Gross_Open"]),
                number(row["Gross_Close"]),
                number(row["Net_Open"]),
                number(row["Net_Close"]),
                number(row["Advances"]),
                number(row["Tier1"]),
                number(row["Tier2"]),
                number(row["CAR"]),
                number(row["Interest_Earned"]),
                number(row["Interest_Expended"]),
                number(row["NII"]),
                number(row["Other_Income"]),
                number(row["Operating_Expenses"]),
                number(row["Net_Profit"]),
                number(row["Assets"]),
                number(row["Previous_Assets"]),
                number(row["Borrowings"]),
                number(row["Capital"]),
                number(row["Reserves"]),
                number(row["Deposits"])
            ))

    cursor.executemany("""
        INSERT INTO banks (id, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
    """, list(banks))

    cursor.executemany("""
        INSERT INTO financial_records (
            bank_id, year, gross_open, gross_close,
            net_open, net_close, advances, tier1, tier2, car,
            interest_earned, interest_expended, nii,
            other_income, operating_expenses, net_profit,
            assets, previous_assets, borrowings, capital,
            reserves, deposits
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            gross_open = VALUES(gross_open),
            gross_close = VALUES(gross_close),
            net_open = VALUES(net_open),
            net_close = VALUES(net_close),
            advances = VALUES(advances),
            tier1 = VALUES(tier1),
            tier2 = VALUES(tier2),
            car = VALUES(car),
            interest_earned = VALUES(interest_earned),
            interest_expended = VALUES(interest_expended),
            nii = VALUES(nii),
            other_income = VALUES(other_income),
            operating_expenses = VALUES(operating_expenses),
            net_profit = VALUES(net_profit),
            assets = VALUES(assets),
            previous_assets = VALUES(previous_assets),
            borrowings = VALUES(borrowings),
            capital = VALUES(capital),
            reserves = VALUES(reserves),
            deposits = VALUES(deposits)
    """, records)

    connection.commit()

    print("\nRBI DATA IMPORT SUCCESSFUL!")
    print("Unique banks:", len(banks))
    print("Financial records:", len(records))
    print("LCR: left NULL (not supplied)")

except Exception as error:
    if connection and connection.is_connected():
        connection.rollback()
    print("\nIMPORT FAILED:", error)

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
