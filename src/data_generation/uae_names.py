import random

FIRST_NAMES = [
    "Ahmed", "Mohammed", "Abdullah", "Hassan", "Omar",
    "Ali", "Khalid", "Saeed", "Yousef", "Faisal",
    "Salem", "Nasser", "Majid", "Rashid"
]

LAST_NAMES = [
    "Al Mansoori", "Al Nuaimi", "Al Mazrouei", "Al Zaabi",
    "Al Amiri", "Al Shamsi", "Al Suwaidi", "Al Falasi",
    "Al Ketbi", "Al Dhaheri"
]

def generate_local_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
