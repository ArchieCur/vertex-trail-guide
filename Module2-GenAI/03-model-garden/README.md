# Module 03: The Model Garden (OSS Models)

Vertex AI isn't just for Google models.  
The **Model Garden** allows you to deploy Open Source Software (OSS) models like Llama, Mistral, and BERT.  
However, the "Rules of Engagement" change significantly when you leave the Gemini ecosystem.

## 🧠 Cognitive Friction: Serverless vs. Provisioned
This is the single biggest mental hurdle for new Vertex users.

* **Gemini (Serverless):** You call an API, pay per token, and Google handles the "servers." It is always on and scales instantly.
* **Model Garden (Provisioned):** To use an OSS model, you must **deploy it to an Endpoint**.
  - This creates a dedicated virtual server (GPU/TPU) that stays on until you delete it.
* **The Friction:** Users often deploy a Llama model to "test it out," forget to delete the endpoint,
  and wake up to a massive bill for a GPU that sat idle all night.

---

## 🛠️ Essential Code: Deploying from the Garden
To use an OSS model, you follow a three-step pattern: **Select -> Deploy -> Predict.**

```python
from google.cloud import aiplatform
```

# 1. Point to the Model in the Garden  

<model_name = "projects/cloudaidemo/locations/us-central1/publishers/meta/models/llama3-8b">

# 2. Deploy to an Endpoint (This creates a 'Server')  

# WARNING: This starts the billing clock!  
```python
endpoint = aiplatform.Endpoint.create(display_name="llama3-endpoint")

deployed_model = endpoint.deploy(
    model=model_name,
    machine_type="n1-standard-8",
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1
)
```

# 3. Get a Prediction

```python
response = endpoint.predict(instances=[{"prompt": "Explain black holes like I'm five."}])
print(response.predictions)
```
## 🧠 **Model Friction: The "Prompt Format" Trap**  
*The Problem:*  

- Gemini is trained to understand a standard ChatSession object.  
- OSS models like Llama or Mistral often expect a very specific "Prompt Template" (e.g., [INST] ... [/INST]).

*The Reality:* 

- If you send a raw string to an OSS model without its preferred delimiters, the output will be incoherent or "hallucinated."

*The Fix:* 
**Always** check the Model Garden card for the specific Prompt Template required by that publisher.

## ⚠️ Pitfalls  

**The "Zombie" Endpoint**

*The Problem:*   
Forgetting to "Undeploy" a model.    
*The Pitfall:*   
- In Gemini, you pay $0 if you don't use it.  
- In Model Garden, you pay for the GPU every hour it is active, regardless of usage.    
**Best Practice:** Always include a cleanup() block in your code to endpoint.delete(force=True).

**The "Cold Start" Wait**  

*The Problem:*   
Expecting an OSS model to be ready in milliseconds.  
*The Pitfall:*   
- When you first deploy a model, Vertex has to provision hardware and load weights (often 20GB+).  
- This can take 5–15 minutes.    
**Best Practice:** Warn users that "Deploying" is a background task, not an instant one.

## 🆘 What to do if you get in trouble  

**Quota Errors:**  
- If you see Quota exceeded for L4 GPUs, you likely need to request a quota increase in the Google Cloud Console.
- Most new accounts start with 0 GPU quota.

**Model Won't Deploy:**

- Check the machine_type.
- Many OSS models require specific GPUs (like A100s) to fit their memory requirements.
- A small n1-standard instance will crash during the loading phase.
