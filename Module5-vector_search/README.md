# Module 05: Vector Search (RAG)

To give Gemini "long-term memory" or access to your private data, we use **Vector Search**. This is the core of Retrieval-Augmented Generation (RAG). 

## 🧠 Cognitive Friction: The "Database" vs. "Engine" Gap
Most developers expect Vector Search to work like PostgreSQL: you insert a row, and it is immediately searchable. Vertex AI Vector Search is different.

* **The Human Logic:** "I just uploaded my embeddings; why can't I query them yet?"
* **The System Reality:** Vertex Vector Search is a high-performance math engine. It requires a **Building** phase (to create the index) and a **Deployment** phase (to put that index on a server).
* **The Friction:** These phases are not instant. Building an index can take 10-30 minutes, and deploying it to an endpoint can take another 15. You cannot "live-stream" data into a searchable index without specific, more complex configurations.

---

## 🛠️ Essential Code: The Vector Workflow
The pattern for Vector Search is: **Embed -> Index -> Deploy -> Query.**

```python
from google.cloud import aiplatform

# 1. Create the Index (The 'Book' of data)
# Note: 'contents_delta_uri' is a GCS bucket containing your .json embeddings
my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name="trail-guide-index",
    contents_delta_uri="gs://your-bucket/embeddings/",
    dimensions=768, # Matches Gemini/Vertex embedding models
    approximate_neighbors_count=10,
)

# 2. Create an Index Endpoint (The 'Server')
my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name="trail-guide-endpoint",
    public_endpoint_enabled=True
)

# 3. Deploy (This starts the billing clock!)
my_index_endpoint.deploy_index(
    index=my_index,
    deployed_index_id="trail_guide_deployed_v1"
)
```

## 🧠 Model Friction: The "Distance" Misconception  

**The Problem:**  
- The search returns results that are "mathematically close" but "contextually useless."

**The Reality:**  
- The model doesn't know meaning; it knows proximity.
- If your embedding model and your LLM aren't aligned, or if your "chunks" of text are too small, the search will find the right words but the wrong answer.

**The Fix:**  
- Always include Metadata Filters. Don't just search by "vibe"; search by {"category": "legal"} to force the engine into the right neighborhood.

## ⚠️ Pitfalls

1. **The "Dimension Mismatch"**
**The Problem:**
- Your code crashes during index creation.

**The Pitfall:**
- You created embeddings with a model that outputs 1536 dimensions, but you told your Vertex Index to expect 768.

**Best Practice:** Double-check your embedding model documentation (e.g., text-embedding-004 uses 768 by default).


2. **The "Deployment" Cost**
**The Problem:**
- Leaving an Index Endpoint active,
 
**The Pitfall:**
  - Just like the Model Garden, a deployed index uses dedicated nodes.
  - If you leave it deployed, it will charge you hourly.

**Best Practice:** For learning, always undeploy the index when you are finished testing.

## 🆘 What to do if you get in trouble  

1. Index is "Stuck" in Building:
- Large indexes take time.
- Check the Batch Predictions or Vector Search tab in the console to see the progress bar.

2. Empty Results:
- Ensure your JSON files in GCS follow the exact format: {"id": "1", "embedding": [0.1, 0.2, ...],
"restricts": [...]}. A single missing comma will cause the indexer to skip the file silently.
