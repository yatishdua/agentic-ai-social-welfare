from openpyxl import Workbook
import random

from src.utils.path_utils import project_path


def generate_assets_excel(applicant_id):
    wb = Workbook()
    ws = wb.active
    ws.title = "Assets_Liabilities"

    ws.append(["Type", "Description", "Value"])

    assets = [
        ("Asset", "Savings", random.randint(20000, 80000)),
        ("Asset", "Vehicle", random.randint(30000, 120000))
    ]

    liabilities = [
        ("Liability", "Personal Loan", random.randint(0, 50000))
    ]

    for row in assets + liabilities:
        ws.append(row)

    file_path = project_path(
        "data", "raw", "assets_excel",
        f"{applicant_id}_assets.xlsx"
    )

    wb.save(str(file_path))
    return file_path
