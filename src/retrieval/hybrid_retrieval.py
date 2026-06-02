from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
from dotenv import load_dotenv
import faiss
import pickle
import numpy as np
import os

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# -----------------------------
# Neo4j Connection
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

# -----------------------------
# Load FAISS Index
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
# User Question
# -----------------------------

question = input(
    "Ask a compliance question: "
)

# -----------------------------
# Create Query Embedding
# -----------------------------

query_embedding = model.encode(
    [question]
)

query_embedding = np.array(
    query_embedding,
    dtype=np.float32
)

# -----------------------------
# Search FAISS
# -----------------------------

distances, indices = index.search(
    query_embedding,
    1
)

best_match = metadata[
    indices[0][0]
]

# -----------------------------
# Display Best Match
# -----------------------------

print("\n")
print("=" * 60)
print("BEST MATCH FROM FAISS")
print("=" * 60)

print(
    f"\nType: {best_match['type']}"
)

print(
    f"Title: {best_match['title']}"
)

# -----------------------------
# Neo4j Traversal
# -----------------------------

with driver.session() as session:

    if best_match["type"] == "Article":

        result = session.run("""
        MATCH (a:Article {number:$id})

        OPTIONAL MATCH (a)-[:IMPLEMENTED_BY]->(p)

        OPTIONAL MATCH (p)-[:REFERENCES]->(d)

        RETURN
        a.title AS article,
        a.content AS article_content,

        p.name AS policy,
        p.content AS policy_content,

        d.name AS procedure,
        d.content AS procedure_content
        """,
        id=best_match["id"])

    elif best_match["type"] == "Policy":

        result = session.run("""
        MATCH (p:Policy {name:$name})

        OPTIONAL MATCH (a)-[:IMPLEMENTED_BY]->(p)

        OPTIONAL MATCH (p)-[:REFERENCES]->(d)

        RETURN
        a.title AS article,
        a.content AS article_content,

        p.name AS policy,
        p.content AS policy_content,

        d.name AS procedure,
        d.content AS procedure_content
        """,
        name=best_match["id"])

    else:

        result = session.run("""
        MATCH (d:Procedure {name:$name})

        OPTIONAL MATCH (p)-[:REFERENCES]->(d)

        OPTIONAL MATCH (a)-[:IMPLEMENTED_BY]->(p)

        RETURN
        a.title AS article,
        a.content AS article_content,

        p.name AS policy,
        p.content AS policy_content,

        d.name AS procedure,
        d.content AS procedure_content
        """,
        name=best_match["id"])

    records = list(result)

driver.close()

# -----------------------------
# Display Results
# -----------------------------

print("\n")
print("=" * 60)
print("GRAPH CONTEXT")
print("=" * 60)

for record in records:

    print("\n" + "=" * 60)

    print(
        f"\nArticle:\n{record['article']}"
    )

    print(
        f"\nPolicy:\n{record['policy']}"
    )

    print(
        f"\nProcedure:\n{record['procedure']}"
    )

    print("\n--- ARTICLE CONTENT ---\n")

    if record["article_content"]:
        print(
            record["article_content"][:500]
        )

    print("\n--- POLICY CONTENT ---\n")

    if record["policy_content"]:
        print(
            record["policy_content"][:500]
        )

    print("\n--- PROCEDURE CONTENT ---\n")

    if record["procedure_content"]:
        print(
            record["procedure_content"][:500]
        )