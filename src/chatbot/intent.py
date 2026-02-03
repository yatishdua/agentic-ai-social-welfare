def detect_intent(user_text: str) -> str:
    text = user_text.strip().lower()

    # 1️⃣ Explicit menu selection (HIGHEST PRIORITY)
    if text == "1":
        return "APPLY_WELFARE"

    if text == "2":
        return "KNOW_CRITERIA"

    # 2️⃣ Keyword-based detection
    if "criteria" in text or "eligible" in text:
        return "KNOW_CRITERIA"

    if "apply" in text or "welfare" in text:
        return "APPLY_WELFARE"

    # 3️⃣ Safe default
    return "APPLY_WELFARE"
