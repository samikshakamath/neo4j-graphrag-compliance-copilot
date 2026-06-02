from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

with driver.session() as session:

    # -----------------------------
    # GDPR Regulation
    # -----------------------------

    session.run("""
    CREATE (:Regulation {
        name:'GDPR',
        jurisdiction:'EU'
    })
    """)

    # -----------------------------
    # GDPR Articles
    # -----------------------------

    articles = [
        ("5", "Principles relating to processing of personal data"),
        ("6", "Lawfulness of processing"),
        ("17", "Right to erasure"),
        ("25", "Data protection by design and by default"),
        ("28", "Processor"),
        ("32", "Security of processing"),
        ("44", "General principle for transfers")
    ]

    for article_num, title in articles:

        session.run("""
        MATCH (g:Regulation {name:'GDPR'})
        CREATE (a:Article {
            number:$number,
            title:$title
        })
        CREATE (g)-[:HAS_ARTICLE]->(a)
        """,
        number=article_num,
        title=title)

    # -----------------------------
    # Policy Nodes
    # -----------------------------

    policies = [
        "Employee Data Policy",
        "Customer Privacy Policy",
        "Vendor Management Policy"
    ]

    for policy in policies:

        session.run("""
        CREATE (:Policy {
            name:$name
        })
        """,
        name=policy)

    # -----------------------------
    # Procedure Node
    # -----------------------------

    session.run("""
    CREATE (:Procedure {
        name:'Data Deletion Procedure'
    })
    """)

    # -----------------------------
    # Article -> Policy Relationships
    # -----------------------------

    mappings = [
        ("5", "Employee Data Policy"),
        ("6", "Employee Data Policy"),
        ("17", "Customer Privacy Policy"),
        ("25", "Customer Privacy Policy"),
        ("28", "Vendor Management Policy"),
        ("32", "Employee Data Policy"),
        ("44", "Vendor Management Policy")
    ]

    for article_num, policy_name in mappings:

        session.run("""
        MATCH (a:Article {number:$article})
        MATCH (p:Policy {name:$policy})
        CREATE (a)-[:IMPLEMENTED_BY]->(p)
        """,
        article=article_num,
        policy=policy_name)

    # -----------------------------
    # Policy -> Procedure
    # -----------------------------

    session.run("""
    MATCH (p:Policy {name:'Customer Privacy Policy'})
    MATCH (d:Procedure {name:'Data Deletion Procedure'})
    CREATE (p)-[:REFERENCES]->(d)
    """)

print("Compliance graph created successfully!")

driver.close()