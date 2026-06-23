from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    TODO — Milestone 1:

    Before writing any code, complete specs/classifier-spec.md. The blank fields
    there are the decisions that drive this implementation — prompt design, tier
    definitions, output format, and edge case handling.

    Your implementation should:
      1. Build a prompt using your tier definitions that asks the LLM to classify
         the question and explain its reasoning
      2. Send a single chat completion request (no tools, no history)
      3. Parse the tier and reason out of the raw response text
      4. Validate the tier against VALID_TIERS; fall back to "caution" if the
         response can't be parsed or the tier isn't recognized
      5. Return {"tier": ..., "reason": ...}

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned

    The three tiers:
          - "safe"    : routine, low-risk repairs most homeowners can handle safely
          - "caution" : doable with care, but mistakes have real cost or mild risk
          - "refuse"  : high-risk repairs that require a licensed professional —
                        mistakes can cause fire, flooding, injury, or structural damage
    """
    system_msg = (
        "You are a safety classifier for home repair questions. "
        "Classify each question into exactly one of three tiers: safe, caution, refuse.\n\n"
        "safe — routine maintenance, worst case is cosmetic damage.\n"
        "caution — doable for motivated homeowner, mistakes have real cost but "
        "no fire/flood/injury risk. Component swap at existing location.\n"
        "refuse — amateur mistake can cause fire, flooding, structural failure, "
        "injury, or death; or local code requires a permit. Includes any new wire "
        "run, any gas work, any wall removal without engineer sign-off, water heater "
        "replacement.\n\n"
        "Return your answer in this exact format:\n"
        "Tier: <one of: safe, caution, refuse>\n"
        "Reason: <one sentence>"
    )
    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": question},
            ],
            max_tokens=200,
        )
        text = response.choices[0].message.content
        tier, reason = "caution", text.strip()  # fail-closed default
        for line in text.splitlines():
            cleaned = line.strip().lower().lstrip("*-` ").rstrip("*` .,:")
            if cleaned.startswith("tier:"):
                candidate = cleaned.split("tier:", 1)[1].strip().strip("*`. ,\"'")
                if candidate in VALID_TIERS:
                    tier = candidate
            elif cleaned.startswith("reason:"):
                reason = line.split(":", 1)[1].strip()
        return {"tier": tier, "reason": reason}
    except Exception as e:
        return {"tier": "refuse", "reason": f"Classifier error — failing closed: {e}"}
