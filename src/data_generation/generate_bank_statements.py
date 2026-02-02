from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import random
import pandas as pd

from src.utils.path_utils import project_path


def generate_transactions(monthly_income):
    transactions = []
    balance = random.randint(2000, 8000)

    for i in range(20):
        date = datetime.now() - timedelta(days=random.randint(1, 90))
        amount = random.randint(50, 500)

        if i == 5:  # salary credit
            transactions.append((date, "Salary Credit", monthly_income))
            balance += monthly_income
        else:
            transactions.append((date, "Debit", -amount))
            balance -= amount

    return transactions


def generate_bank_statement(applicant_id, applicant_name, monthly_income):
    file_path = project_path(
        "data", "raw", "bank_statements",
        f"{applicant_id}_bank_statement.pdf"
    )

    c = canvas.Canvas(str(file_path), pagesize=A4)
    c.setFont("Helvetica", 10)

    c.drawString(50, 800, f"Bank Statement")
    c.drawString(50, 780, f"Account Holder: {applicant_name}")
    c.drawString(50, 760, f"Account Number: {random.randint(10000000,99999999)}")

    y = 720
    c.drawString(50, y, "Date")
    c.drawString(150, y, "Description")
    c.drawString(350, y, "Amount")

    y -= 20

    for date, desc, amt in generate_transactions(monthly_income):
        c.drawString(50, y, date.strftime("%d-%m-%Y"))
        c.drawString(150, y, desc)
        c.drawString(350, y, str(amt))
        y -= 15

        if y < 50:
            c.showPage()
            y = 750

    c.save()
    return file_path
