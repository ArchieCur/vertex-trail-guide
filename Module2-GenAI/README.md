**Module 02: Generative AI (Gemini)**

In Vertex AI, the **Gemini 1.5** models are the primary engines for reasoning, transformation, and generation. This module covers how to move from "chatting" to building reliable, structured applications.

## 🧠 **Model Friction: The "Persona vs. Probability" Gap**
Users often expect the model to "know" their intent instinctively. However, models operate on **Token Logic**.

* **The "Vague Directive" Friction:**
    * *Human:* "Make this professional."
    * *Model Reality:* Does "professional" mean a legal brief, a corporate email, or a scientific paper? 
    * *The Fix:* Use **System Instructions** to define the exact format, tone, and constraints.
* **The "Safety Block" Friction:**
    * *Human:* "Why did my code crash? The model just didn't answer."
    * *Model Reality:* A safety filter triggered, and the model returned an empty "candidate."
    * *The Fix:* Always check `finish_reason` before accessing `response.text`.

---

## 🛠️ Essential Code: Structured JSON Output
In production, you rarely want a "paragraph" from a model. You want **data**. Gemini 1.5 allows you to force a JSON response.
```

```python
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Define the "Rulebook"
system_instruction = "You are a data extraction bot. Return ONLY valid JSON."

model = GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=[system_instruction]
)

# Force JSON via Mime Type
config = GenerationConfig(
    response_mime_type="application/json",
    temperature=0.1 # Keep it low for structural integrity
)

prompt = "Extract the city and population from: The city of Austin has 961,855 people."

response = model.generate_content(prompt, generation_config=config)
print(response.text)
```

⚠️ **Pitfalls**

1. **The "Candidate" Error**
The Problem: Accessing response.text when a prompt is blocked.
The Pitfall: If the model blocks a response for safety, response.text will raise an exception.
Best Practice: Check if response.candidates[0].finish_reason == "SAFETY": before parsing.

2. **Flash vs. Pro Usage**
The Problem: Using gemini-1.5-pro for simple tasks.
The Pitfall: Pro is 10x more expensive than Flash. Flash is optimized for speed and high-volume tasks like summarization.
Best Practice: Use Flash by default. Only upgrade to Pro if the logic fails.

🆘 **What to do if you get in trouble**

**Model Not Found:** 

-Ensure your region is us-central1. Many new versions of Gemini are not yet available in all regions.

**Empty Responses:**

- Check your SafetySettings. If your prompt contains words that could be misinterpreted (even in a technical context),  
the model might refuse to answer. Set safety filters to BLOCK_ONLY_HIGH for testing.
