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
        staging_bucket=STAGING_BUCKET
    )
    print(f"✅ Vertex AI initialized in {LOCATION}")

if __name__ == "__main__":
    initialize_vertex()