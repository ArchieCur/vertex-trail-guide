# Module 04: MLOps & Vertex Pipelines

In previous modules, we ran code manually. In a production environment, you need an automated **factory**. Vertex AI Pipelines (powered by Kubeflow) allows you to orchestrate complex workflows, but it introduces a significant shift in how you write code.

## 🧠 Cognitive Friction: The "Island" Problem
This is the most common hurdle for developers transitioning from scripts to pipelines.

* **The Human Logic:** "I defined a variable `model_resource_name` in Step 1. Surely Step 2 can see it because they are in the same script file."
* **The System Reality:** Each step (component) in a pipeline runs in its own **completely isolated container**. 
* **The Friction:** You cannot pass Python variables between steps like a normal script. You must explicitly **serialize** data into "Artifacts" or "Outputs" that are stored in Cloud Storage and then "downloaded" by the next container.

---

## 🛠️ Essential Code: The Minimal Pipeline
This script defines a two-step pipeline. Notice how we must tell each function exactly what packages it needs, because every "Island" starts with nothing.

```python
from kfp import dsl
from kfp import compiler
from google.cloud import aiplatform

# 1. Define a 'Component' (Island #1)
@dsl.component(packages_to_install=["pandas"])
def build_message(name: str) -> str:
    # We must import inside the function because the container 
    # doesn't see the global scope!
    return f"Hello {name}, your pipeline is running!"

# 2. Define a second 'Component' (Island #2)
@dsl.component
def print_message(msg: str):
    print(msg)

# 3. Define the 'Pipeline' (The Map between Islands)
@dsl.pipeline(name="trail-guide-hello-world")
def basic_pipeline(recipient: str):
    # Step 1 execution
    first_step = build_message(name=recipient)
    
    # Step 2 execution (Passing the OUTPUT of step 1 to step 2)
    second_step = print_message(msg=first_step.output)

# 4. Compile and Run
compiler.Compiler().compile(pipeline_func=basic_pipeline, package_path="pipeline.json")

job = aiplatform.PipelineJob(
    display_name="hello-world-pipeline-job",
    template_path="pipeline.json",
    parameter_values={"recipient": "Vertex Learner"}
)
job.run()
```

## 🧠 Model/System Friction: "Dependency Hell"  

**The Problem:**  
- Your pipeline fails with ModuleNotFoundError: No module named 'google-cloud-aiplatform'.
**The Reality:**
- Even though the pipeline is running inside Google Cloud, the default container is "naked."
- It doesn't have your local libraries installed.

**The Fix:**  
- You must use the packages_to_install argument in the @dsl.component decorator for every single step that requires a library.

## ⚠️ Pitfalls

1. **The "Storage" Tax**

**The Problem:**  
- Pipelines create a massive trail of metadata and small files.
  
**The Pitfall:**
- Every time a pipeline runs, it saves artifacts to your STAGING_BUCKET.
- If you run hundreds of tests, these thousands of tiny files can slowly increase your storage costs.

**Best Practice:** Set a Lifecycle Policy on your Google Cloud Storage bucket to auto-delete objects older than 30 days in your staging folders.

2. **The "Local Testing" Mirage**

**The Problem:**  
- Trying to "run" the pipeline function locally like a normal Python script.  
**The Pitfall:**  
- The @dsl.pipeline decorator changes how the function behaves; calling it locally won't execute the steps, it will just return a pipeline object.

**Best Practice:** Keep your core logic in plain Python functions. Test those independently. Wrap them in @dsl.component only when the logic is 100% solid.

## 🆘 What to do if you get in trouble

- **Check the Visualizer:** Go to Vertex AI > Pipelines in the console. If a step is red, click it and select the Logs tab.
- 99% of errors are ImportError or PermissionDenied.

### Service Account Permissions  
- If your pipeline fails to write results, ensure the Vertex AI Custom Code Service Agent has the Storage Object Admin role in your project.
