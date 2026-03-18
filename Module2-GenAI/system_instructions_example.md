# 🔍 Case Study: A Completed System Instruction

To give you a clear "mental model" of a professional Vertex AI system instruction, here is a breakdown of a **Technical Support Triage Bot**. 

Notice how it avoids "fluff" and focuses on **classification rules** and **output structures**.

---

## 📝 The "Gold Standard" Example

**System Instruction:**
> **ROLE**: You are a Tier-1 Technical Support Triage Specialist for a SaaS platform.
>
> **CONTEXT**: You analyze incoming customer emails to determine priority and category before a human agent sees them.
>
> **TASK**: 
> 1. Categorize the issue into: [BILLING, TECHNICAL_BUG, FEATURE_REQUEST, ACCOUNT_ACCESS].
> 2. Assign a Priority: [P1 - Urgent, P2 - High, P3 - Normal].
> 3. Extract the 'Product Version' mentioned. If not found, return 'NULL'.
>
> **CONSTRAINTS**:
> - Never respond to the customer directly. 
> - If the user mentions "Login" or "Password," the category MUST be ACCOUNT_ACCESS.
> - If the user mentions "Down" or "Crash," the priority MUST be P1.
> - Be objective. Do not summarize the customer's emotions.
>
> **OUTPUT FORMAT**:
> Return ONLY a JSON object with these keys: 
> {
>  "category": string,
>  "priority": string,
>  "version": string,
>  "is_urgent": boolean
> }

---

## 🧠 Why This "Hits Right" for the Model

1. **Explicit Triggers:** By saying "If the user mentions X, the category MUST be Y," you are reducing the model's cognitive load. It doesn't have to "think"; it just has to "match."
2. **Defined Vocabulary:** Giving the model a specific list (e.g., `[BILLING, TECHNICAL_BUG...]`) prevents it from making up its own categories like "Money issues" or "Software problem."
3. **Negative Constraints:** The instruction "Never respond to the customer directly" is vital. Without it, the model might try to be "helpful" and write a reply, which would break your automated JSON pipeline.

---

## 🛠️ Implementation Pattern

In your code, you would implement this using a multi-line string to maintain readability:

```python
from vertexai.generative_models import GenerativeModel

triage_instructions = """
[Paste the block above here]
"""

model = GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=[triage_instructions]
)
