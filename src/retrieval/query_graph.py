from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# -----------------------------
# Connect to Neo4j
# -----------------------------

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

# -----------------------------
# User Input
# -----------------------------

article_number = input(
    "Enter GDPR article number: "
)

# -----------------------------
# Neo4j Query
# -----------------------------

query = """
MATCH (a:Article {number:$article})

OPTIONAL MATCH (a)-[:IMPLEMENTED_BY]->(p:Policy)

OPTIONAL MATCH (p)-[:REFERENCES]->(d:Procedure)

RETURN
a.title AS article_title,
a.content AS article_content,
p.name AS policy_name,
p.content AS policy_content,
d.name AS procedure_name,
d.content AS procedure_content
"""

# -----------------------------
# Execute Query
# -----------------------------

with driver.session() as session:

    result = session.run(
        query,
        article=article_number
    )

    records = list(result)

    if len(records) == 0:

        print("\nArticle not found.")

    else:

        for record in records:

            print("\n===================================")
            print(f"GDPR ARTICLE {article_number}")
            print("===================================")

            print(
                f"\nTitle:\n{record['article_title']}"
            )

            print(
                f"\nRelated Policy:\n{record['policy_name']}"
            )

            print(
                f"\nRelated Procedure:\n{record['procedure_name']}"
            )

            print("\n===================================")
            print("ARTICLE CONTENT")
            print("===================================")

            print(
                record["article_content"][:1000]
            )

            print("\n===================================")
            print("POLICY CONTENT")
            print("===================================")

            if record["policy_content"]:

                print(
                    record["policy_content"][:1000]
                )

            print("\n===================================")
            print("PROCEDURE CONTENT")
            print("===================================")

            if record["procedure_content"]:

                print(
                    record["procedure_content"][:1000]
                )

driver.close()