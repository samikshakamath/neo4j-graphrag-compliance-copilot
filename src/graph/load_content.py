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


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


with driver.session() as session:

    # -----------------------------
    # GDPR Articles
    # -----------------------------

    article_numbers = [
        "5", "6", "17", "25", "28", "32", "44"
    ]

    for article_num in article_numbers:

        file_path = (
            f"data/gdpr_articles/article_{article_num}.txt"
        )

        content = read_file(file_path)

        session.run(
            """
            MATCH (a:Article {number:$number})
            SET a.content = $content
            """,
            number=article_num,
            content=content
        )

    # -----------------------------
    # Policies
    # -----------------------------

    policy_files = {
        "Employee Data Policy":
            "data/employee_data_policy.txt",

        "Customer Privacy Policy":
            "data/customer_privacy_policy.txt",

        "Vendor Management Policy":
            "data/vendor_management_policy.txt"
    }

    for policy_name, file_path in policy_files.items():

        content = read_file(file_path)

        session.run(
            """
            MATCH (p:Policy {name:$name})
            SET p.content = $content
            """,
            name=policy_name,
            content=content
        )

    # -----------------------------
    # Procedure
    # -----------------------------

    content = read_file(
        "data/data_deletion_procedure.txt"
    )

    session.run(
        """
        MATCH (p:Procedure {
            name:'Data Deletion Procedure'
        })
        SET p.content = $content
        """,
        content=content
    )

print("Content loaded successfully!")

driver.close()