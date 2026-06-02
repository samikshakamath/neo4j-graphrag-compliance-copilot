from neo4j import GraphDatabase
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# -----------------------------
# Connect Neo4j
# -----------------------------

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

# -----------------------------
# Load Embedding Model
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

documents = []

# -----------------------------
# Retrieve Articles
# -----------------------------

with driver.session() as session:

    result = session.run("""
    MATCH (a:Article)
    RETURN
        a.number AS id,
        a.title AS title,
        a.content AS content
    """)

    for record in result:

        documents.append({
            "type": "Article",
            "id": record["id"],
            "title": record["title"],
            "content": record["content"]
        })

    result = session.run("""
    MATCH (p:Policy)
    RETURN
        p.name AS name,
        p.content AS content
    """)

    for record in result:

        documents.append({
            "type": "Policy",
            "id": record["name"],
            "title": record["name"],
            "content": record["content"]
        })

    result = session.run("""
    MATCH (p:Procedure)
    RETURN
        p.name AS name,
        p.content AS content
    """)

    for record in result:

        documents.append({
            "type": "Procedure",
            "id": record["name"],
            "title": record["name"],
            "content": record["content"]
        })

driver.close()

# -----------------------------
# Create Text List
# -----------------------------

texts = []

for doc in documents:

    text = f"""
    {doc['title']}

    {doc['content']}
    """

    texts.append(text)

# -----------------------------
# Generate Embeddings
# -----------------------------

embeddings = model.encode(texts)

embeddings = np.array(
    embeddings,
    dtype=np.float32
)

# -----------------------------
# Create FAISS Index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(embeddings)

# -----------------------------
# Save Files
# -----------------------------

faiss.write_index(
    index,
    "vector_index.faiss"
)

with open(
    "metadata.pkl",
    "wb"
) as f:

    pickle.dump(
        documents,
        f
    )

print(
    f"Indexed {len(documents)} documents."
)