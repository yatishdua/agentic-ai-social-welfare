from rag.rag_chain import answer_policy_question
import os

def handle_turn(state, validation, intake=None,policy_vectorstore=None):
    intent = validation.intent

    # ---------- OUT OF SCOPE ----------
    if intent == "OUT_OF_SCOPE":
        return "I can only help with economic welfare."

    # ---------- ASK CRITERIA (ANYTIME) ----------
    if intent == "ASK_CRITERIA":
        result = answer_policy_question(
            policy_vectorstore,
            validation.raw_answer
        )

        response = result["answer"]

        if result["sources"]:
            response += "\n\n**Sources:**\n"
            for i, s in enumerate(result["sources"], 1):
                response += f"{i}. {os.path.basename(s['source'])}\n"

        return response

    # ---------- START APPLY ----------
    if intent == "START_APPLY" and state["mode"] != "APPLY":
        state["mode"] = "APPLY"
        state["phase"] = "INTAKE"
        return "Sure. Let’s start your application.\n\nWhat is your employment status? (employed or unemployed)"

    # ---------- APPLY FLOW ----------
    if state["mode"] == "APPLY":

        # INTAKE PHASE
        if state["phase"] == "INTAKE" and intake:
            state["ui_data"] = intake.ui_data.model_dump(exclude_none=True)

            if intake.next_question:
                return intake.next_question

            # Intake complete → move to review
            if not intake.missing_fields:
                state["phase"] = "REVIEW"
                summary = "\n".join(
                    f"- {k}: {v}" for k, v in (state["ui_data"] or {}).items()
                )
                return (
                    "### Please review your details:\n"
                    f"{summary}\n\n"
                    "Do you want to submit this application? (Yes/No)"
                )

        # REVIEW PHASE
        if state["phase"] == "REVIEW":
            if intent == "ANSWER":
                state["confirm_submit"] = validation.raw_answer.lower() in ["yes", "y"]
                if state["confirm_submit"]:
                    state["phase"] = "UPLOAD"
                    return "Great. Please upload your documents."
                else:
                    state["phase"] = "INTAKE"
                    return "Okay. Let’s continue editing your application."

        # UPLOAD PHASE
        if state["phase"] == "UPLOAD":
            return "Waiting for document uploads…"

    return "How can I help you?"
