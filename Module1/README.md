# Module 01: Foundations & The "Invisible" Setup

Before you can build with Vertex AI, you have to navigate the "Invisible Setup"—the permissions, initializations, and cloud resources that the SDK assumes you already have. This module covers the bulletproof way to start any Vertex project.

## 🧭 The Core Setup
To follow the samples in this guide, ensure you have:
1. **A Google Cloud Project** with billing enabled.
2. **Vertex AI API Enabled:** `gcloud services enable aiplatform.googleapis.com`
3. **Local Authentication:** Run `gcloud auth application-default login` in your terminal. 

---

## 🛠️ Essential Code: The "Bulletproof" Init
This script initializes both the **Generative AI** and **Core AIPlatform** SDKs. It ensures you have a "landing zone" (Staging Bucket) for your artifacts.

```python
import vertexai
from google.cloud import aiplatform

PROJECT_ID = "your-project-id"  
LOCATION = "us-central1" # Recommended default
STAGING_BUCKET = f"gs://{PROJECT_ID}-vertex-staging"

def initialize_vertex():
    # Initialize the GenAI-specific SDK (for Gemini)
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # Initialize the Core SDK (for Pipelines, Training, and Metadata)
    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION,
```

🧠 **Cognitive Friction & Patterns**

The "Dual SDK" Confusion: There are actually two ways to interact with Vertex in Python: vertexai and google.cloud.aiplatform.

**Friction:** You'll see tutorials using both interchangeably.

**Pattern:** 

- Use vertexai for anything involving Gemini/LLMs.
- Use aiplatform for "infrastructure" tasks like creating endpoints or running pipelines.

**The "Ghost Bucket" Trap:**

If you don't define a staging_bucket during init, many commands will work fine until you try to upload a model or run a batch job.
Then, they will fail with a vague 400 error because there is no "scratchpad" in the cloud for the SDK to use.

⚠️ **Pitfalls**

1. **The Region Lock**

The Problem: You set your region to us-east1 because it's close to you.
The Pitfall: New models (like Gemini 1.5 Pro or Flash updates) often roll out to us-central1 first. You will get a 404: Model not found error even if the model exists globally.
Best Practice: Always start your learning in us-central1.

2. **The "Default Credentials" Headache**
   
The Problem: Running code in a Docker container or a CI/CD pipeline.
The Pitfall: The code works on your laptop but fails in the container because application-default login only exists on your host machine.
Best Practice: Use Service Account JSON keys only for production; use Workload Identity for everything else.

🆘 **What to do if you get in trouble**

- Check Permissions: If you get a 403 Forbidden, go to the IAM console and ensure your user/service account has the Vertex AI User role.
- Verify the API: Run gcloud services list --enabled | grep aiplatform. If it's empty, the API isn't on.
- Bucket Access: Ensure your STAGING_BUCKET actually exists. The SDK will not always create it for you; you may need to run <gsutil mb gs://your-bucket-name> first.

```python
        staging_bucket=STAGING_BUCKET
    )
    print(f"✅ Vertex AI initialized in {LOCATION}")

if __name__ == "__main__":
    initialize_vertex()
```
