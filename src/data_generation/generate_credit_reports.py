from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random

from src.utils.path_utils import project_path


def generate_credit_report(applicant_id, applicant_name):
    credit_score = random.randint(550, 800)
    open_loans = random.randint(0, 3)

    file_path = project_path(
        "data", "raw", "credit_reports",
        f"{applicant_id}_credit_report.pdf"
    )

    c = canvas.Canvas(str(file_path), pagesize=A4)
    c.setFont("Helvetica", 11)

    c.drawString(50, 800, "Credit Bureau Report")
    c.drawString(50, 770, f"Name: {applicant_name}")
    c.drawString(50, 740, f"Credit Score: {credit_score}")
    c.drawString(50, 710, f"Open Loans: {open_loans}")
    c.drawString(50, 680, f"Default History: {'Yes' if credit_score < 600 else 'No'}")

    c.save()
    return file_path
