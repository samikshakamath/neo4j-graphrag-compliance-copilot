from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
from dotenv import load_dotenv
from openai import OpenAI

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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# -----------------------------
# Neo4j Connection
# -----------------------------

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

# -----------------------------
# Embedding Model
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# Load FAISS
# -----------------------------

index = faiss.read_index(
    "vector_index.faiss"
)

with open(
    "metadata.pkl",
    "rb"
) as f:

    metadata = pickle.load(f)


# =====================================================
# MAIN FUNCTION
# =====================================================

def get_compliance_answer(question):

    # -----------------------------
    # Semantic Search
    # -----------------------------

    query_embedding = model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    distances, indices = index.search(
        query_embedding,
        1
    )

    best_match = metadata[
        indices[0][0]
    ]

    # -----------------------------
    # Neo4j Retrieval
    # -----------------------------

    context = ""
    sources = set()
    reasoning_paths = []

    with driver.session() as session:

        if best_match["type"] == "Procedure":

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

        records = list(result)

    # -----------------------------
    # Context + Citations + Paths
    # -----------------------------

    for record in records:

        article = record["article"]
        policy = record["policy"]
        procedure = record["procedure"]

        if article:
            sources.add(
                f"GDPR Article - {article}"
            )

        if policy:
            sources.add(
                f"Policy - {policy}"
            )

        if procedure:
            sources.add(
                f"Procedure - {procedure}"
            )

        path = []

        if article:
            path.append(article)

        if policy:
            path.append(policy)

        if procedure:
            path.append(procedure)

        if len(path) > 1:

            reasoning_paths.append(
                " → ".join(path)
            )

        if record["article_content"]:
            context += "\n\nARTICLE:\n"
            context += record["article_content"][:1000]

        if record["policy_content"]:
            context += "\n\nPOLICY:\n"
            context += record["policy_content"][:1000]

        if record["procedure_content"]:
            context += "\n\nPROCEDURE:\n"
            context += record["procedure_content"][:1000]

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = f"""
    You are an enterprise compliance assistant.

    Use ONLY the supplied context.

    If the answer is not present in the context,
    say so clearly.

    Question:
    {question}

    Context:
    {context}

    Provide:

    1. Direct Answer

    2. Compliance Explanation

    Do NOT generate your own source list.
    """

    # -----------------------------
    # OpenAI Generation
    # -----------------------------

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return (
        answer,
        reasoning_paths,
        sorted(list(sources))
    )