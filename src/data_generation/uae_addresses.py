import random

EMIRATES = {
    "Abu Dhabi": ["Al Reem Island", "Mussafah", "Al Khalidiya", "Al Bateen"],
    "Dubai": ["Deira", "Bur Dubai", "Jumeirah", "Al Barsha", "Business Bay"],
    "Sharjah": ["Al Majaz", "Al Nahda", "Al Qasimia"],
    "Ajman": ["Al Nuaimiya", "Al Rashidiya"],
    "Ras Al Khaimah": ["Al Nakheel", "Al Dhait"],
    "Fujairah": ["Dibba", "Al Faseel"],
    "Umm Al Quwain": ["Al Salama", "Al Raas"]
}

def generate_uae_address():
    emirate = random.choice(list(EMIRATES.keys()))
    area = random.choice(EMIRATES[emirate])
    po_box = random.randint(10000, 99999)

    return {
        "emirate": emirate,
        "area": area,
        "address": f"{area}, {emirate}, PO Box {po_box}"
    }
