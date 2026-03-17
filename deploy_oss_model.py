import os
import sys
from google.cloud import aiplatform

# 1. Configuration - Change these to match your environment
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
# Example: Llama 3 8B from the Model Garden
MODEL_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/meta/models/llama3-8b"

def deploy_and_test_oss_model():
    """
    Deploys an OSS model from the Garden, runs a test, and then cleans up.
    """
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    print("🚀 Starting deployment. This can take 5-15 minutes...")
    
    try:
        # Create an Endpoint
        endpoint = aiplatform.Endpoint.create(display_name="llama3-trail-guide-endpoint")

        # Deploy the Model
        # NOTE: We use a T4 GPU here as it's often the easiest to get quota for.
        deployed_model = endpoint.deploy(
            model=MODEL_RESOURCE_NAME,
            machine_type="n1-standard-8",
            accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=1,
            deploy_request_timeout=1800 # 30 minute timeout for large weights
        )

        print("✅ Model deployed successfully.")

        # 2. The Prediction (Note the specific dictionary format OSS models often expect)
        test_instance = {
            "prompt": "What is the primary difference between a star and a planet?",
            "max_tokens": 100,
            "top_p": 0.9,
            "temperature": 0.7
        }

        print("📡 Sending test prediction...")
        response = endpoint.predict(instances=[test_instance])
        print(f"🤖 Model Output: {response.predictions}")

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
    
    finally:
        # THE 'WHAT TO DO IF YOU GET IN TROUBLE' SAFETY NET
        # This block ensures that even if the code crashes, we try to delete the 
        # endpoint to stop the billing clock.
        if 'endpoint' in locals():
            print("🧹 Cleaning up: Deleting endpoint to stop billing...")
            endpoint.delete(force=True)
            print("✨ Cleanup complete.")

if __name__ == "__main__":
    if PROJECT_ID == "your-project-id":
        print("⚠️ Please edit the PROJECT_ID in the script before running.")
        sys.exit(1)
    deploy_and_test_oss_model()