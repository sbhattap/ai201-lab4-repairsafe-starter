# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
["safe"    : routine, low-risk repairs most homeowners can handle safely]
```

**caution:**
```
["caution" : doable with care, but mistakes have real cost or mild risk]
```

**refuse:**
```
["refuse"  : high-risk repairs that require a licensed professional —
                    mistakes can cause fire, flooding, injury, or structural damage]
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
[I will ask  the llm to provide an one line reasoning before naming the tier.]
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
[I will ask the llm to output the tier and reason in a JSON format, with keys "tier" and "reason".]
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
["You are a safety classifier for home repair questions. "
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
        "Reason: <one sentence>"]
```

**User message:**
```
["Classify the following home repair question:\n\n"
        "<question>"]
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
[The boundary between "caution" and "refuse" is determined by whether a mistake could lead to significant safety hazards (fire, flooding, injury) or requires professional certification or permits.]
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
[If the LLM response can't be parsed or the tier validation fails, the function will return a default tier of "caution" with a reason indicating that the classification could not be determined. Failing closed (returning "caution") is safer than failing open (returning "safe") because it errs on the side of caution, reducing the risk of providing unsafe advice.]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
[N/A]
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
[N/A]
```
