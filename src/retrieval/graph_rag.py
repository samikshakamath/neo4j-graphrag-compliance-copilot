from neo4j import GraphDatabase
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
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
# OpenAI Model
# -----------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
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
# Retrieve Context
# -----------------------------

with driver.session() as session:

    result = session.run(
        query,
        article=article_number
    )

    record = result.single()

driver.close()

# -----------------------------
# Check Article Exists
# -----------------------------

if record is None:

    print("Article not found.")
    exit()

# -----------------------------
# Build Context
# -----------------------------

context = f"""
GDPR Article:
{record['article_title']}

Article Content:
{record['article_content']}

Policy:
{record['policy_name']}

Policy Content:
{record['policy_content']}

Procedure:
{record['procedure_name']}

Procedure Content:
{record['procedure_content']}
"""

# -----------------------------
# Prompt
# -----------------------------

prompt = f"""
You are an enterprise compliance assistant.

Using ONLY the information provided below,
explain how AcmeTech complies with the GDPR requirement.

Context:

{context}

Provide:

1. Summary
2. Relevant Policy
3. Relevant Procedure
4. Compliance Risk
5. Recommendation

Do not invent information.
Only use the supplied context.
"""

# -----------------------------
# LLM Response
# -----------------------------

response = llm.invoke(prompt)

# -----------------------------
# Output
# -----------------------------

print("\n")
print("=" * 60)
print("COMPLIANCE ANALYSIS")
print("=" * 60)
print("\n")

print(response.content)