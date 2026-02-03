def enablement_agent(state):
    recommendations = []

    eligibility = state.get("eligibility_result", {})
    ui = state.get("ui_data", {})
    validation = state.get("validation_result", {})

    # If already eligible → still provide optional support
    if eligibility.get("eligible") is True:
        recommendations.append({
            "type": "INFO",
            "message": "You are eligible for economic welfare. You may also explore skill development programs for long-term stability."
        })

    # Income-related recommendations
    if eligibility.get("reason") == "INCOME_TOO_HIGH":
        recommendations.append({
            "type": "FINANCIAL_PLANNING",
            "message": "Consider financial counseling or expense optimization programs to reduce effective income burden."
        })

    if eligibility.get("reason") == "INCOME_TOO_LOW":
        recommendations.append({
            "type": "UPS KILLING",
            "message": "You may benefit from vocational training or skill development programs to increase employability."
        })

    # Employment-based
    if ui.get("employment_status") == 0:
        recommendations.append({
            "type": "JOB_SUPPORT",
            "message": "We recommend enrolling in job placement or employment assistance programs."
        })

    # Disability-based
    if ui.get("disability_flag") == 1:
        recommendations.append({
            "type": "SPECIAL_ASSISTANCE",
            "message": "You may qualify for disability-specific welfare and support services."
        })

    # Validation issues
    if validation.get("income_mismatch"):
        recommendations.append({
            "type": "DOCUMENT_CORRECTION",
            "message": "Please ensure that your declared income matches official bank documents."
        })

    state["enablement_recommendations"] = {
        "count": len(recommendations),
        "recommendations": recommendations
    }

    state["audit_log"].append(
        f"Enablement recommendations generated: {len(recommendations)}"
    )

    return state
