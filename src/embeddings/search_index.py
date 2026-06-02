from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

# -----------------------------
# Load Model
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# Load Index
# -----------------------------

index = faiss.read_index(
    "vector_index.faiss"
)

with open(
    "metadata.pkl",
    "rb"
) as f:

    metadata = pickle.load(f)

# -----------------------------
# User Query
# -----------------------------

query = input(
    "Ask a compliance question: "
)

# -----------------------------
# Create Embedding
# -----------------------------

query_embedding = model.encode(
    [query]
)

query_embedding = np.array(
    query_embedding,
    dtype=np.float32
)

# -----------------------------
# Search
# -----------------------------

k = 3

distances, indices = index.search(
    query_embedding,
    k
)

# -----------------------------
# Results
# -----------------------------

print("\nTop Matches:\n")

for idx in indices[0]:

    doc = metadata[idx]

    print("=" * 50)

    print(
        f"Type: {doc['type']}"
    )

    print(
        f"Title: {doc['title']}"
    )

    print("\nPreview:\n")

    print(
        doc["content"][:300]
    )

    print("\n")